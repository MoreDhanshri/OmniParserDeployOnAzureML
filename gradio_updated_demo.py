from typing import Optional

import gradio as gr
import numpy as np
import torch
from PIL import Image
import io
import base64, os
from utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img

yolo_model = get_yolo_model(model_path='weights/icon_detect/best.pt')
caption_model_processor = get_caption_model_processor(model_name="florence2", model_name_or_path="weights/icon_caption_florence")

MARKDOWN = """
# OmniParser for Pure Vision Based General GUI Agent 🔥
<div>
    <a href="https://arxiv.org/pdf/2408.00203">
        <img src="https://img.shields.io/badge/arXiv-2408.00203-b31b1b.svg" alt="Arxiv" style="display:inline-block;">
    </a>
</div>

OmniParser is a screen parsing tool to convert general GUI screen to structured elements. 
"""

DEVICE = torch.device('cuda')

def process(
    image_input,
    box_threshold,
    iou_threshold,
    use_paddleocr
) -> Optional[Image.Image]:
    image_save_path = 'imgs/saved_image_demo.png'
    image_input.save(image_save_path)
    image = Image.open(image_save_path)
    box_overlay_ratio = image.size[0] / 3200
    draw_bbox_config = {
        'text_scale': 0.8 * box_overlay_ratio,
        'text_thickness': max(int(2 * box_overlay_ratio), 1),
        'text_padding': max(int(3 * box_overlay_ratio), 1),
        'thickness': max(int(3 * box_overlay_ratio), 1),
    }

    ocr_bbox_rslt, is_goal_filtered = check_ocr_box(image_save_path, display_img=False, output_bb_format='xyxy', goal_filtering=None, easyocr_args={'paragraph': False, 'text_threshold': 0.9}, use_paddleocr=use_paddleocr)
    text, ocr_bbox = ocr_bbox_rslt

    dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(image_save_path, yolo_model, BOX_TRESHOLD=box_threshold, output_coord_in_ratio=False, ocr_bbox=ocr_bbox, draw_bbox_config=draw_bbox_config, caption_model_processor=caption_model_processor, ocr_text=text, use_local_semantics=True, iou_threshold=0.1)
    image = Image.open(io.BytesIO(base64.b64decode(dino_labled_img)))
    parsed_content_list = '\n'.join(parsed_content_list)
    
    formatted_output = []
    for idx, (key, coordinates) in enumerate(label_coordinates.items()):
            # Extract coordinates
        x, y, width, height = map(int, coordinates)
            
            # Parse label and type from parsed_content_list
        content = parsed_content_list[idx]
        content_parts = content.split(": ")
        type_label = content_parts[0]  # Type (e.g., 'Text Box ID 0')
        name_label = content_parts[1] if len(content_parts) > 1 else ""  # Name (e.g., 'Q Search')
            
            # Format output line
        formatted_output.append(
            f"Element {idx}: x={x}, y={y}, width={width}, height={height}, {name_label}, {type_label}"
        )
    
    
    #label_coordinates_str = str(label_coordinates)

    return image, parsed_content_list, formatted_output

with gr.Blocks() as demo:
    gr.Markdown(MARKDOWN)
    with gr.Row():
        with gr.Column():
            image_input_component = gr.Image(type='pil', label='Upload image')
            box_threshold_component = gr.Slider(label='Box Threshold', minimum=0.01, maximum=1.0, step=0.01, value=0.05)
            iou_threshold_component = gr.Slider(label='IOU Threshold', minimum=0.01, maximum=1.0, step=0.01, value=0.1)
            use_paddleocr_component = gr.Checkbox(label='Use PaddleOCR', value=True)
            submit_button_component = gr.Button(value='Submit', variant='primary')
        with gr.Column():
            image_output_component = gr.Image(type='pil', label='Image Output')
            text_output_component = gr.Textbox(label='Parsed screen elements', placeholder='Text Output')
            label_coordinates_output_component = gr.Textbox(label='Label Coordinates', placeholder='Label Coordinates Output')

    submit_button_component.click(
        fn=process,
        inputs=[
            image_input_component,
            box_threshold_component,
            iou_threshold_component,
            use_paddleocr_component
        ],
        outputs=[image_output_component, text_output_component, label_coordinates_output_component]
    )

demo.launch(share=True, server_port=7861, server_name='0.0.0.0')