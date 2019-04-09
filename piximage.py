from PIL import Image
import argparse
import shutil
import os


def check_size(size_x: int, size_y: int, tile_w: int, tile_h: int):
	boxes = []
	v_x = size_x // tile_w
	delta_x = size_x % tile_w
	v_y = size_y // tile_h
	delta_y = size_y % tile_h
	for column in range(0, v_y):
		for row in range(0, v_x + 1):
			x = row * tile_w
			y = column * tile_h
			boxes.append((x, y, x + tile_w, y + tile_h))
		x += tile_w
		y += tile_h
		boxes.append((x, y, x + delta_x, y + tile_h))

	y = v_y * tile_h
	for row in range(0, v_x):
		x = row * tile_w
		boxes.append((x, y, x + tile_w, y + delta_y))
	boxes.append((x, y, x + delta_x, y + delta_y))
	return boxes


def get_avg_color(pixels: list):
	rgb = []
	size = len(pixels)
	if size == 0:
		return [0, 0, 0]
	i = 0
	while i < 3:
		v = 0
		for color in pixels:
			v += color[i]
		rgb.append(v // size)
		i += 1
	return rgb


def convert(image: str, out_image: str, tile_w: int, tile_h: int):
	try:
		shutil.rmtree('tiles/')
		shutil.rmtree('colors/')
	except:
		print('')
	os.mkdir('tiles')
	os.mkdir('colors')
	im = Image.open(image)
	size_x, size_y = im.size
	if size_x < tile_w or size_y < tile_h:
		print("Change the size of tiles.")
		quit()

	regions = []
	boxes = check_size(size_x, size_y, tile_w, tile_h)
	for i in boxes:
		region = im.crop(i)
		print(region)
		region.save("tiles/{}_{}_{}_{}.jpg".format(i[0], i[1], i[2], i[3]))
		pixels = list(region.getdata())
		avg_color = get_avg_color(pixels)
		print(avg_color)
		for column in range(region.size[0]):
			for row in range(region.size[1]):
				region.putpixel((column, row), (avg_color[0], avg_color[1], avg_color[2]))
		region.save("colors/{}_{}_{}_{}.jpg".format(i[0], i[1], i[2], i[3]))
		regions.append(region)
	for f in range(len(boxes)):
		im.paste(regions[f], boxes[f])
	im.save(out_image)
	im.show()


def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type=str)
	parser.add_argument('--output', type=str)
	parser.add_argument('--weight', type=int)
	parser.add_argument('--height', type=int)
	return parser


if __name__ == '__main__':
	parser = createParser()
	n = parser.parse_args()
	convert(n.input, n.output, n.weight, n.height)
