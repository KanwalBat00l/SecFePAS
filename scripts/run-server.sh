#!/usr/bin/env bash
# scripts/run-server.sh

. scripts/common.sh

if [ $# -ne 2 ]; then
  echo -e "${RED}Please specify the network to run.${NC}"
  echo "Usage: run-server.sh [cheetah|SCI_HE] [sqnet|sqnet_quantized|resnet50|resnet50_quantized]"
  exit 1
fi

MODE=$1     # cheetah or SCI_HE
NET=$2      # sqnet, sqnet_quantized, resnet50, or resnet50_quantized

if ! contains "cheetah SCI_HE" "$MODE"; then
  echo -e "Usage: run-server.sh ${RED}[cheetah|SCI_HE]${NC} [sqnet|sqnet_quantized|resnet50|resnet50_quantized]"
  exit 1
fi

if ! contains "sqnet sqnet_quantized resnet50 resnet50_quantized" "$NET"; then
  echo -e "Usage: run-server.sh [cheetah|SCI_HE] ${RED}[sqnet|sqnet_quantized|resnet50|resnet50_quantized]${NC}"
  exit 1
fi

# pick up the corresponding weights file (quantized or not)
WEIGHT_FILE=( pretrained/${NET}_*_input_weights_fixedpt_scale_*.inp )
if [ ! -f "${WEIGHT_FILE[0]}" ]; then
  echo -e "${RED}Could not find weights file for '${NET}' in pretrained/.${NC}"
  echo "Expected something like '${NET}_*_input_weights_fixedpt_scale_*.inp'"
  exit 1
fi

mkdir -p data

echo -e "Using weights file: ${GREEN}${WEIGHT_FILE[0]}${NC}"
echo -e "Running ${GREEN}build/bin/${NET}-${MODE}${NC}  (this may take a while)..."

cat "${WEIGHT_FILE[0]}" \
  | build/bin/${NET}-${MODE} \
      r=1 \
      ell=${SS_BITLEN} \
      nt=${NUM_THREADS} \
      port=${SERVER_PORT} \
  2>&1 | tee "${MODE}-${NET}_server.log"

echo -e "Done.  Server log → ${GREEN}${MODE}-${NET}_server.log${NC}"
