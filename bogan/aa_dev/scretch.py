import numpy as np
import pandas as pd
df = pd.DataFrame(np.random.randint(3, 26, size=(20,3)))

print(df)
cats = pd.cut(df[0], 10)
print(cats)
