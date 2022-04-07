from __future__ import annotations
from typing import Final as const

#[LackExtract]2022/04/01:抽出用のセレクターを辞書でまとめる。
    #ジャンルごとに異なるので、データ形式は下記のとおりとする。
    #{"項目名":{
        # "ヘアサロン":"セレクター", 
        # "ネイル・まつげサロン":"セレクター",
        # "リラクサロン":"セレクター", 
        # "エステサロン":"セレクター"
        # }
    # }
    

SELECTOR:const[dict[str, dict[str, str]]]  = {
    "table_menu": {            
            "ヘアサロン":"#mainContents > div.mT30 > table.slnDataTbl > tbody > tr > th",
            "ネイル・まつげサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > th",
            "リラクサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > th",
            "エステサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > th",
        },
        "table_value": {
            "ヘアサロン":"#mainContents > div.mT30 > table.slnDataTbl > tbody > tr > td",
            "ネイル・まつげサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > td",
            "リラクサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > td",
            "エステサロン":"#mainContents > div.mT30 > table.wFull > tbody > tr > td"
        },
        "store_name": {
            "ヘアサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh.hMin120 > div > p.detailTitle > a",
            "ネイル・まつげサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.detailTitle > a",
            "リラクサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.detailTitle > a",
            "エステサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.detailTitle > a"
        },
        "stname_kana": {
            "ヘアサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh.hMin120 > div > p.fs10.fgGray",
            "ネイル・まつげサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.fs10.fgGray",
            "リラクサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.fs10.fgGray",
            "エステサロン":"#mainContents > div.detailHeader.cFix.pr > div > div.pL10.oh > div > p.fs10.fgGray"
        },
        "tel": {
            "ヘアサロン":"#mainContents > table > tbody > tr > td",
            "ネイル・まつげサロン":"#mainContents > table > tbody > tr > td",
            "リラクサロン":"#mainContents > table > tbody > tr > td",
            "エステサロン":"#mainContents > table > tbody > tr > td"
        },
        
        "pankuzu": {
            "ヘアサロン":"#preContents > ol > li",
            "ネイル・まつげサロン":"#preContents > ol > li",
            "リラクサロン":"#preContents > ol > li",
            "エステサロン":"#preContents > ol > li"
        },
        "header_img": {
            "ヘアサロン":"#jsiNavCarousel > div > img",
            "ネイル・まつげサロン":"#jsiNavCarousel > div > img",
            "リラクサロン":"#jsiNavCarousel > div > img",
            "エステサロン":"#jsiNavCarousel > div > img"
        },
        "slide_img": {
            "ヘアサロン":"#mainContents > div.pH10.mT25 > div:nth-child(1) > div > div.slnTopImg.jscThumbCarousel > div.slnTopImgCarouselWrap.jscThumbWrap > ul > li",
            "ネイル・まつげサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > div > div.slnTopImg.jscThumbCarousel > div.slnTopImgCarouselWrap.jscThumbWrap > ul > li",
            "リラクサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > div > div.slnTopImg.jscThumbCarousel > div.slnTopImgCarouselWrap.jscThumbWrap > ul > li",
            "エステサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > div > div.slnTopImg.jscThumbCarousel > div.slnTopImgCarouselWrap.jscThumbWrap > ul > li"
        },
        "catchcopy": {
            "ヘアサロン":"#mainContents > div.pH10.mT25 > div:nth-child(1) > p > b > strong",
            "ネイル・まつげサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > p > b > strong",
            "リラクサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > p > b > strong",
            "エステサロン":"#mainContents > div.pH10.mT30 > div:nth-child(1) > p > b > strong"
        },
}