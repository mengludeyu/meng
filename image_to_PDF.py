import os
from PIL import Image
from fpdf import FPDF


def convert_images_to_pdfs(input_folder, output_folder, page_size='A4', dpi=300):
    """
    将文件夹中的图片批量转换为高分辨率PDF

    参数:
        input_folder: 包含图片的文件夹路径
        output_folder: 保存PDF的文件夹路径
        page_size: PDF页面大小('A3', 'A4', 'A5', 'letter', 'legal' 或自定义元组(宽,高)单位mm)
        dpi: 输出PDF的分辨率(每英寸点数)，默认300
    """
    # 支持的图片格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

    # 预定义的页面大小(mm)
    page_sizes = {
        'A3': (297, 420),
        'A4': (210, 297),
        'A5': (148, 210),
        'letter': (216, 279),
        'legal': (216, 356)
    }

    # 获取页面尺寸
    if isinstance(page_size, str) and page_size.lower() in page_sizes:
        page_width, page_height = page_sizes[page_size.lower()]
    elif isinstance(page_size, (tuple, list)) and len(page_size) == 2:
        page_width, page_height = page_size
    else:
        raise ValueError("不支持的页面尺寸，请使用'A3','A4','A5','letter','legal'或自定义(宽,高)元组(单位mm)")

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 检查文件是否为支持的图片格式
        if filename.lower().endswith(supported_formats):
            try:
                # 构建完整文件路径
                input_path = os.path.join(input_folder, filename)

                # 生成输出PDF文件名(与图片同名)
                pdf_name = os.path.splitext(filename)[0] + '.pdf'
                output_path = os.path.join(output_folder, pdf_name)

                # 打开图片文件
                with Image.open(input_path) as img:
                    # 转换为RGB模式(避免某些格式如PNG的透明度问题)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # 计算图片宽高比
                    img_ratio = img.width / img.height

                    # 计算PDF页面尺寸(转换为点，1mm=2.83464567点)
                    pdf_page_width = page_width * 2.83464567
                    pdf_page_height = page_height * 2.83464567

                    # 确定图片在PDF中的显示尺寸(保持比例)
                    if (pdf_page_width / pdf_page_height) > img_ratio:
                        # 以高度为基准
                        img_width = pdf_page_height * img_ratio
                        img_height = pdf_page_height
                    else:
                        # 以宽度为基准
                        img_width = pdf_page_width
                        img_height = pdf_page_width / img_ratio

                    # 计算居中位置
                    x_pos = (pdf_page_width - img_width) / 2
                    y_pos = (pdf_page_height - img_height) / 2

                    # 临时保存为高质量JPEG
                    temp_path = os.path.join(output_folder, 'temp.jpg')
                    img.save(temp_path, 'JPEG', quality=95, dpi=(dpi, dpi))

                    # 使用FPDF创建PDF
                    pdf = FPDF(unit='pt', format=(pdf_page_width, pdf_page_height))
                    pdf.add_page()
                    pdf.image(temp_path, x_pos, y_pos, img_width, img_height)
                    pdf.output(output_path, 'F')

                    # 删除临时文件
                    os.remove(temp_path)

                print(f"成功转换: {filename} -> {pdf_name} (页面尺寸: {page_width}x{page_height}mm)")

            except Exception as e:
                print(f"转换 {filename} 失败: {str(e)}")


if __name__ == "__main__":
    # 输入文件夹(包含图片)
    input_folder = "input_images"  # 替换为你的图片文件夹路径

    # 输出文件夹(保存PDF)
    output_folder = "output_pdfs"  # 替换为你想保存PDF的文件夹路径

    # PDF页面大小(可选'A3','A4','A5','letter','legal'或自定义(宽,高)元组(单位mm))
    page_size = 'A4'  # 例如: 'A4' 或 (200, 300)

    # 调用转换函数
    convert_images_to_pdfs(
        input_folder=input_folder,
        output_folder=output_folder,
        page_size=page_size,
        dpi=300
    )