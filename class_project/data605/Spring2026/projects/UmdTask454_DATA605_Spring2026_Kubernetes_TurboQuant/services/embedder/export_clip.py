import sys

import open_clip
import torch


def main(out_path):
    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    model.eval()
    dummy = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model.visual,
        dummy,
        out_path,
        input_names=["image"],
        output_names=["embedding"],
        dynamic_axes={"image": {0: "batch"}, "embedding": {0: "batch"}},
        opset_version=14,
    )
    print(f"exported {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "clip_visual.onnx")
