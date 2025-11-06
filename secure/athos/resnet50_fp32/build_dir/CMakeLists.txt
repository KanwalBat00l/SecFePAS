
                cmake_minimum_required (VERSION 3.0)
                project (BUILD_IT)
                find_package(SCI REQUIRED PATHS "/home/kbatool/work/EzPC/Athos/../SCI/build/install")
                add_executable(resnet50_fp32_SCI_HE.out /gpfs/home5/kbatool/work/deliverables/secure/athos/resnet50_fp32/resnet50_fp32_41_sci_HE0.cpp)
                target_link_libraries(resnet50_fp32_SCI_HE.out SCI::SCI-HE)
            