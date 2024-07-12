from webptools import cwebp
from webptools import gifwebp
from webptools import webpmux_animate


from io import BytesIO
from PIL import Image, ImageSequence
from django.core.files.base import ContentFile


# def resize_image(image):
#     img = Image.open(image)
#
#     if img.format == 'GIF' and img.is_animated:
#         frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
#         webp_data = webpmux.WebPAnimEncoder(frames, loop=0).as_webp()
#
#         new_name = f"{image.name.rsplit('.', 1)[0]}.webp"
#         return ContentFile(webp_data, name=new_name)
#
#     else:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         img = img.resize((300, 300), Image.Resampling.LANCZOS)
#
#         image_io = BytesIO()
#         img.save(image_io, format='WEBP')
#
#         image_data = image_io.getvalue()
#
#         new_name = f"{image.name.rsplit('.', 1)[0]}.webp"
#         return ContentFile(image_data, name=new_name)



# class resize_image:
#     def convert_image(self):
#         print(cwebp(input_image="python_logo.jpg", output_image="python_logo.webp",
#                 option="-q 80", logging="-v"))
#
#     def convert_gif(self):
#         print(gifwebp(input_image="linux_logo.gif", output_image="linux_logo.webp",
#                       option="-q 80", logging="-v"))
#
#     def convert_gif_animation(self):
#         input = ["./frames/tmp-0.webp +100", "./frames/tmp-1.webp +100",
#                  "./frames/tmp-2.webp +100"]
#         print(webpmux_animate(input_images=input, output_image="anim_container.webp",
#                               loop="10", bgcolor="255,255,255,255"))