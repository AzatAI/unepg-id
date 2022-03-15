# unepg-id






`pyinstaller --clean --name UniBadge -i logo.ico .\interface.py`

`pyinstaller --clean --name UniBadge -i logo.ico --windowed .\interface.py`


``` python
datas=[
                 ('media\\bar\\*.txt', '.\\media\\bar\\'),
                 ('static\\fonts\\*.ttf', '.\\static\\fonts\\'),
                 ('static\\images\\*.png', '.\\static\\images\\'),
                 ('cards\\*', '.\\cards\\')
                 ],
```

`pyinstaller ./XXXX.spec`

``` python

datas=[
     ('media/bar/*.txt', './media/bar/'),
     ('static/fonts/*.ttf', './static/fonts/'),
     ('static/images/*.png', './static/images/'),
     ('cards/*', './cards/')
     ],
```