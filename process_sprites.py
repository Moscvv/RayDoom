from PIL import Image

# Open images
sprite1 = Image.open("attack_0.png").convert("RGBA")
sprite2 = Image.open("attack_1.png").convert("RGBA")

# Merge using alpha compositing
merged_sprite = Image.alpha_composite(sprite1, sprite2)

# Save merged sprite
merged_sprite.save("attack222.png")
