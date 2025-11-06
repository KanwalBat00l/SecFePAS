#!/usr/bin/env bash
# scripts/run-client.sh

. scripts/common.sh

if [ $# -ne 2 ]; then
  echo -e "${RED}Please specify the network to run.${NC}"
  echo "Usage: run-client.sh [cheetah|SCI_HE] [sqnet|sqnet_quantized|resnet50|resnet50_quantized]"
  exit 1
fi

MODE=$1     
NET=$2      
if ! contains "cheetah SCI_HE" "$MODE"; then
  echo -e "Usage: run-client.sh ${RED}[cheetah|SCI_HE]${NC} [sqnet|sqnet_quantized|resnet50|resnet50_quantized]"
  exit 1
fi

if ! contains "sqnet sqnet_quantized resnet50 resnet50_quantized" "$NET"; then
  echo -e "Usage: run-client.sh [cheetah|SCI_HE] ${RED}[sqnet|sqnet_quantized|resnet50|resnet50_quantized]${NC}"
  exit 1
fi

# pick up the client's input file (quantized or not, fp32 vs fp16)
INPUT_FILE=( pretrained/${NET}_*_input_fixedpt_scale_*.inp )
if [ ! -f "${INPUT_FILE[0]}" ]; then
  echo -e "${RED}Could not find client input file for '${NET}' in pretrained/.${NC}"
  echo "Expected something like '${NET}_*_input_fixedpt_scale_*.inp'"
  exit 1
fi

mkdir -p data

echo -e "Using client input file: ${GREEN}${INPUT_FILE[0]}${NC}"
echo -e "Running ${GREEN}build/bin/${NET}-${MODE}${NC} ..."

cat "${INPUT_FILE[0]}" \
  | build/bin/${NET}-${MODE} \
      r=2 \
      ell=${SS_BITLEN} \
      nt=${NUM_THREADS} \
      ip=${SERVER_IP} \
      port=${SERVER_PORT} \
  2>&1 | tee "${MODE}-${NET}_client.log"

echo -e "Done.  Client log → ${GREEN}${MODE}-${NET}_client.log${NC}"
