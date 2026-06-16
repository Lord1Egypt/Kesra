extends RefCounted
class_name ProceduralTexture

## Generates flat-color textures at runtime so gameplay nodes (paddle, ball, bricks, drops)
## render without needing any art assets on disk yet. Swap for real sprites later — nothing
## else in the codebase needs to change since these are just ImageTextures.

static func make_rect(width: int, height: int, color: Color) -> ImageTexture:
	var img := Image.create(max(1, width), max(1, height), false, Image.FORMAT_RGBA8)
	img.fill(color)
	return ImageTexture.create_from_image(img)

static func make_circle(diameter: int, color: Color) -> ImageTexture:
	var d: int = max(2, diameter)
	var img := Image.create(d, d, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var radius: float = d / 2.0
	var center := Vector2(radius, radius)
	for y in range(d):
		for x in range(d):
			if Vector2(x + 0.5, y + 0.5).distance_to(center) <= radius:
				img.set_pixel(x, y, color)
	return ImageTexture.create_from_image(img)
