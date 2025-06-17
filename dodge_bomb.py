import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル（横方向、縦方向の画面内判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面の中
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate  # 横方向、縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に,半透明の黒い画面上に「Game Over」と表示し,
    泣いているこうかとん画像を貼り付ける関数
    引数： screen (pg.Surface): 描画先の画面 Surface。
    戻り値：None: 値は返さない。画面に描画するだけ。
    """
    kknaki_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    kknaki_rct = kknaki_img.get_rect()
    kknaki_rct.center = 757, 261
    kknaki_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    kknaki_rct2 = kknaki_img2.get_rect()
    kknaki_rct2.center = 357, 261
    blo_img = pg.Surface((1100, 650))
    pg.draw.rect(blo_img, (0, 0, 0), (1100,650,1100,650))
    blo_img.set_alpha(128)
    blo_rct = blo_img.get_rect()
    font_go = pg.font.Font(None, 80)
    txt = font_go.render("Game Over",True, (255, 255, 255))
    screen.blit(txt, [400, 250])
    screen.blit(kknaki_img, kknaki_rct)
    screen.blit(kknaki_img2, kknaki_rct2)
    screen.blit(blo_img, blo_rct)
    
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    関数内で加速度の段階と画像の拡大のリストの作成
    戻り値→二つのリストをタプルにしたもの
    """
    bb_lst = []
    sbb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_lst.append(bb_img)
    return sbb_accs, bb_lst


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る
    pg.draw.circle(bb_img, (225, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標の乱数
    vx, vy = +5, +5  # 爆弾の移動速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)
            return
            
        bb_accs, bb_imgs = init_bb_imgs()
        bb_img = bb_imgs[min(tmr//500, 9)]  
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])   # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate =check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
