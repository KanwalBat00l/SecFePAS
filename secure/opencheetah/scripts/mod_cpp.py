import re
import sys
import os
import json 

def get_params_from_config(config_filepath):
    try:
        with open(config_filepath, 'r') as f:
            config_data = json.load(f)
        
       
        scale = config_data.get("scale", 12)
        
        target = config_data.get("target", "SCI")
        bitlength = config_data.get("bitlength")
        if bitlength is None:
            if target.upper() == "SCI":
                bitlength = 41 
            else:
                bitlength = 64 
        
     
       
        if target.upper() == "CPP" and bitlength:
             bitlength = 64 if bitlength > 32 else 32
        
        return scale, bitlength
    except FileNotFoundError:
        print(f"ERROR: Config file '{config_filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from '{config_filepath}'.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error reading config file '{config_filepath}': {e}")
        sys.exit(1)


def add_includes_and_defines(cpp_content):
    lines = cpp_content.splitlines()
    new_lines = []
    iostream_added = False
    chrono_added = False
    using_namespace_std_added = False
    use_fused_bn_added = False

    for line in lines:
        new_lines.append(line)
        if "#include <iostream>" in line and not iostream_added:
            if not chrono_added: 
                new_lines.append("#include <chrono>")
                chrono_added = True
            iostream_added = True
        if "using namespace std;" in line and not using_namespace_std_added:
            if not use_fused_bn_added:
                 new_lines.append("#define USE_FUSED_BN 1")
                 use_fused_bn_added = True
            using_namespace_std_added = True
            
  
    if not chrono_added: 
       
        for i, line_content in enumerate(new_lines):
            if line_content.strip().startswith("#include"):
                new_lines.insert(i + 1, "#include <chrono>")
                chrono_added = True
                break
        if not chrono_added:
             new_lines.insert(0, "#include <chrono>")

    if not use_fused_bn_added:
        
        for i, line_content in enumerate(new_lines):
            if "using namespace std;" in line_content:
                new_lines.insert(i + 1, "#define USE_FUSED_BN 1")
                use_fused_bn_added = True
                break
        if not use_fused_bn_added: 
            last_include_idx = -1
            for i, line_content in enumerate(new_lines):
                if line_content.strip().startswith("#include"):
                    last_include_idx = i
            if last_include_idx != -1:
                new_lines.insert(last_include_idx + 1, "#define USE_FUSED_BN 1")
            else: 
                new_lines.insert(1 if chrono_added else 0, "#define USE_FUSED_BN 1")
                
    return "\n".join(new_lines)

def modify_globals(cpp_content, user_scale, user_bitlength):
    lines = cpp_content.splitlines()
    new_lines = []
    bitlength_modified = False
    kscale_added_or_modified = False

    for line in lines:
        
        if re.match(r"^\s*int32_t\s+bitlength\s*=\s*\d+;", line):
            new_lines.append(f"int32_t bitlength = {user_bitlength};")
            bitlength_modified = True
           
            if not kscale_added_or_modified:
                new_lines.append(f"int32_t kScale = {user_scale};")
                kscale_added_or_modified = True
       
        elif re.match(r"^\s*(const\s+)?int32_t\s+kScale\s*=\s*\d+;", line):
            new_lines.append(f"int32_t kScale = {user_scale};") 
            kscale_added_or_modified = True
        else:
            new_lines.append(line)

    
    if not bitlength_modified or not kscale_added_or_modified:
        final_lines = []
        added_globals = False
        for line in new_lines: 
            final_lines.append(line)
            if "using namespace std;" in line and not added_globals:
                if not bitlength_modified:
                    final_lines.append(f"int32_t bitlength = {user_bitlength};")
                if not kscale_added_or_modified:
                    final_lines.append(f"int32_t kScale = {user_scale};")
                added_globals = True
        if not added_globals:
            
            insert_idx = 0
            for i, l in enumerate(final_lines):
                if l.strip().startswith("#include"):
                    insert_idx = i + 1
            if not bitlength_modified:
                final_lines.insert(insert_idx, f"int32_t bitlength = {user_bitlength};")
                insert_idx +=1
            if not kscale_added_or_modified:
                final_lines.insert(insert_idx, f"int32_t kScale = {user_scale};")
        return "\n".join(final_lines)
        
    return "\n".join(new_lines)


def comment_out_hardsigmoid_functions(cpp_content):
    modified_content = cpp_content
    for i in range(1, 5): # HardSigmoid1 to HardSigmoid4
        pattern_start = re.compile(r"^(void\s+HardSigmoid" + str(i) + r"\s*\(.*?\)\s*\{)$", re.MULTILINE)
        new_content_lines = []
        in_hardsigmoid_func = False
        brace_level = 0
        lines = modified_content.splitlines()
        
        for line in lines:
            if in_hardsigmoid_func:
                new_content_lines.append("// " + line)
                brace_level += line.count('{')
                brace_level -= line.count('}')
                if brace_level == 0:
                    in_hardsigmoid_func = False
            else:
                match = pattern_start.search(line)
                if match:
                    in_hardsigmoid_func = True
                    brace_level = line.count('{') - line.count('}')
                    new_content_lines.append("// " + line)
                    if brace_level == 0 and '{' in line and not '}' in line : 
                         brace_level = 1 
                else:
                    new_content_lines.append(line)
        modified_content = "\n".join(new_content_lines)
    return modified_content

def modify_conv_calls_conditional(cpp_content, apply_conv_wrapper_change):
    if not apply_conv_wrapper_change:
        return cpp_content

   
    param_regex_no_comma = r"(?:\s*\([^)]*\)\s*[^,()]*|\s*[^,()]*)" 
    
    
    conv_regex = re.compile(
        r"Conv2DGroupWrapper\s*\("                     
        r"("                                           
            r"(?:(?:" + param_regex_no_comma + r"),\s*){13}" 
        r")"                                           
        r"(?:" + param_regex_no_comma + r",\s*)"       
        r"(.*?\);)"                                    
    , re.MULTILINE)

    def conv_replacer(match):
        first_13_params_with_commas = match.group(1) 
        tensor_args_and_closing = match.group(2)    

       
        return f"Conv2DWrapper({first_13_params_with_commas}{tensor_args_and_closing}"

    modified_content = conv_regex.sub(conv_replacer, cpp_content)
    lines = modified_content.splitlines(keepends=True)
    out_lines = []
    did_first = False
    i = 0

    while i < len(lines):
        line = lines[i]

        if not did_first and "Conv2DWrapper(" in line:
            out_lines.append("#if USE_CHEETAH\n")
            out_lines.append("  kIsSharedInput = false;\n")
            out_lines.append("#endif\n")

            out_lines.append(line)

            count = 0
            j = i + 1
            while j < len(lines) and count < 2:
                out_lines.append(lines[j])
                if "ClearMemSecret4" in lines[j]:
                    count += 1
                j += 1

            out_lines.append("#if USE_CHEETAH\n")
            out_lines.append("  kIsSharedInput = true;\n")
            out_lines.append("#endif\n")


            i = j
            did_first = True
        else:
            out_lines.append(line)
            i += 1

    return "".join(out_lines)

def process_cpp_file(input_filepath, output_filepath, config_filepath, apply_conv_change_for_ot):
    try:
        with open(input_filepath, 'r') as infile:
            content = infile.read()
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_filepath}' not found.")
        sys.exit(1)

    user_scale, user_bitlength = get_params_from_config(config_filepath)
    print(f"INFO: Using scale = {user_scale}, bitlength = {user_bitlength} from config.")

    content = add_includes_and_defines(content)
    print("INFO: Added standard includes and defines.")
    
    content = modify_globals(content, user_scale, user_bitlength)
    print(f"INFO: Globals kScale set to {user_scale} and bitlength to {user_bitlength}.")

    content = comment_out_hardsigmoid_functions(content)
    print("INFO: 'HardSigmoidN' function definitions commented out (if found).")
    
    original_content_before_conv_mod = content
    content = modify_conv_calls_conditional(content, apply_conv_change_for_ot)
    if original_content_before_conv_mod == content:
        if apply_conv_change_for_ot:
             print("INFO: No 'Conv2DGroupWrapper' calls were modified (or pattern not found).")
        else:
            print("INFO: 'Conv2DGroupWrapper' modification skipped as per 'apply_conv_change_for_ot=False'.")
    else:
        print("INFO: 'Conv2DGroupWrapper' calls modified to 'Conv2DWrapper'.")

    try:
        with open(output_filepath, 'w') as outfile:
            outfile.write(content)
        print(f"Processing complete. Modified content written to '{output_filepath}'")
    except IOError:
        print(f"Error: Could not write to output file '{output_filepath}'")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python mod_cpp.py <input_cpp.cpp> <output_cpp.cpp> <athos_config.json> <apply_conv_change_for_OT_target (true/false)>")
        print("  <apply_conv_change_for_OT_target>: 'true' if this C++ is for OpenCheetah's OT/Cheetah target, 'false' for HE target.")
        sys.exit(1)
    
    input_f = sys.argv[1]
    output_f = sys.argv[2]
    config_f = sys.argv[3]
    apply_conv_change_str = sys.argv[4].lower()

    if apply_conv_change_str not in ['true', 'false']:
        print("ERROR: <apply_conv_change_for_OT_target> must be 'true' or 'false'.")
        sys.exit(1)
    
    apply_conv_change = (apply_conv_change_str == 'true')
    
    process_cpp_file(input_f, output_f, config_f, apply_conv_change)
