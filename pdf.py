
import re
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject


def remove_watermark(input_pdf, output_pdf, watermark_text):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        content_object = page['/Contents']
        content = content_object.get_object()

        if isinstance(content, DecodedStreamObject) or isinstance(content, EncodedStreamObject):
            content_stream = content.get_data().decode('utf-8')

            # 使用正则表达式匹配并移除水印文本
            pattern = re.compile(re.escape(watermark_text), re.IGNORECASE)
            modified_content = pattern.sub('', content_stream)

            # 创建新的内容流
            new_content = modified_content.encode('utf-8')
            content_object._data = new_content
            content_object.update()
        writer.add_page(page)
    # 保存新的PDF
    with open(output_pdf, 'wb') as f:
        writer.write(f)


# 使用示例
input_pdf = 'input.pdf'
output_pdf = 'output_without_watermark.pdf'
watermark_text = '网盘分享WPFX.LINK'  # 替换为实际的水印文本

remove_watermark(input_pdf, output_pdf, watermark_text)
