import onnx
import numpy as np
import sys

def fix_dead_filters(onnx_path, inp_in, inp_out):
    model = onnx.load(onnx_path)
    init_sizes = []      
    init_shapes = []      
    for init in model.graph.initializer:
        dims = tuple(init.dims)
        init_shapes.append(dims)
        init_sizes.append(np.prod(dims))

    # 2) Read flat .inp
    data = np.loadtxt(inp_in, dtype=np.int64)
    assert data.size == sum(init_sizes), \
        "Mismatch between ONNX initializers and .inp length"

    out = data.copy()
    offset = 0
    for i, (shape, size) in enumerate(zip(init_shapes, init_sizes)):
        if len(shape) == 4 and shape[2:] == (1,1):
            O, C, H, W = shape
            flat_slice = out[offset:offset+size]
            mat = flat_slice.reshape((O, C))
            sums = mat.sum(axis=1)
            dead = np.where(sums == 0)[0]
            if dead.size:
                print(f"Initializer #{i} shape={shape}: {dead.size} dead filters -> bumping")
                for fidx in dead:
                    mat[fidx, 0] = 1  
                out[offset:offset+size] = mat.flatten()
        offset += size

    np.savetxt(inp_out, out, fmt="%d")
    print("Patched .inp written to", inp_out)


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("Usage: python fix_dead_filters.py model.onnx in.inp out.inp")
        sys.exit(1)
    _, onnx_p, inp_i, inp_o = sys.argv
    fix_dead_filters(onnx_p, inp_i, inp_o)

