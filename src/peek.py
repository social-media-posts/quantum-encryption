import sys
from PIL import Image
from timeline import frame
# usage: peek.py out.png t1 t2 ...
out = sys.argv[1]; ts = [float(x) for x in sys.argv[2:]]
ims = [frame(t).resize((360, 640)) for t in ts]
cols = min(len(ims), 6)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 364, rows * 644), (10, 10, 10))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * 364, (i // cols) * 644))
sheet.save(out)
