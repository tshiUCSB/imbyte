import math
import sys
from PIL import Image, ImageColor

def remove_translucent_pixels(img, threshold=.5, print_count=True):
	img_data = list(img.getdata())
	clean_data = []
	pxl_count = 0
	opaque_count = 0

	for i in range(len(img_data)):
		px = img_data[i]
		if px[3] > 0:
			pxl_count += 1
		if px[3] / 255 > threshold:
			opaque_count += 1
			clean_data.append((255, 255, 255, 255))
		else:
			clean_data.append((0, 0, 0, 0))

	if print_count:
		print("Detected {} non-transparent pixels:\n\t{} pixels are above {}%% opacity\n\t{} pixels are removed\n".format(pxl_count, opaque_count, math.floor(threshold * 100), pxl_count - opaque_count))
	
	clean_img = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
	clean_img.putdata(clean_data)
	return clean_img

def convert_img_to_byte_arr(bin_img):
	img_data = bin_img.getdata()
	byte_arr = []
	for i in range(0, len(img_data), 8):
		byte = 0
		for j in range(8):
			if img_data[i + j][3] > 0:
				byte += 1
			byte << 1
		byte_arr.append(byte)

	byte_arr = bytes(byte_arr)
	return byte_arr
				

if __name__ == "__main__":
	print("==============================")
	in_args = sys.argv
	img_path = ""
	out_path = "output.bin"
	if len(in_args) < 2:
		print("enter path for image:")
		img_path = input()
	else:
		img_path = in_args[1]
	if len(in_args) > 2:
		out_path = in_args[2]


	img = Image.open(img_path)
	bin_img = None
	opac_threshold = .5
	while True:
		bin_img = remove_translucent_pixels(img, opac_threshold)
		bin_img.show()
		print("Adjust opacity threshold(%)?")
		opac = input()
		if opac == "":
			break
		else:
			opac_threshold = float(opac)

	byte_arr = convert_img_to_byte_arr(bin_img)
	out_file = open(out_path, 'wb')
	out_file.write(byte_arr)
	out_file.close()
	print("Successfully exported to {}".format(out_path))
	print("==============================")

	
