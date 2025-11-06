import faulthandler
faulthandler.enable() 
import numpy as np
import onnxruntime as rt
import onnx
import sys, os


def get_numpy_dtype(onnx_model_input):
    if onnx_model_input.type.tensor_type.elem_type == 1:
        return np.float32
    elif onnx_model_input.type.tensor_type.elem_type == 10: 
        return np.float16
    else:
        print(f"Warning: Unsupported ONNX input type {onnx_model_input.type.tensor_type.elem_type}. Defaulting to float32.")
        return np.float32

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_onnx.py <path_to_input.npy> <path_to_onnx_model>")
        sys.exit(1)
        
    input_npy_path = sys.argv[1]
    onnx_model_path = sys.argv[2]

 
    model = onnx.load(onnx_model_path)
    model_input_details = model.graph.input[0] 
    expected_dtype = get_numpy_dtype(model_input_details)
    print(f"Model {os.path.basename(onnx_model_path)} expects input dtype: {expected_dtype}")

    
    input_np_arr = np.load(input_npy_path, allow_pickle=True)
    print(f"Loaded input NPY array with dtype: {input_np_arr.dtype}, shape: {input_np_arr.shape}")

    if input_np_arr.dtype != expected_dtype:
        print(f"Casting input array from {input_np_arr.dtype} to {expected_dtype}")
        input_np_arr_casted = input_np_arr.astype(expected_dtype)
    else:
        input_np_arr_casted = input_np_arr
        
    sess = rt.InferenceSession(onnx_model_path)
    input_name = sess.get_inputs()[0].name
    
    pred_onx = sess.run(None, {input_name: input_np_arr_casted})[0] 
    
    print(f"Output for {os.path.basename(onnx_model_path)} (first 10 values):\n", pred_onx.flatten()[:10])
    
    output_dir = "onnx_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_input_name = os.path.splitext(os.path.basename(input_npy_path))[0]
    base_model_name = os.path.splitext(os.path.basename(onnx_model_path))[0]
    output_name = os.path.join(output_dir, f"{base_input_name}_output_for_{base_model_name}.npy")
    
    np.save(output_name, pred_onx.flatten())
    print(f"Saved output to {output_name}")
