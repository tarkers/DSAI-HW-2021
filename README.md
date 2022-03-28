# DSAI-HW-2021
## 預估3/30-4/13之備轉容量(MW)_Electricity Forecasting
### 名詞定義
#### 備轉容量(MW)
系統運轉淨尖峰能力－系統瞬時尖峰負載(瞬間值)
#### 備轉容量率
（系統運轉淨尖峰供電能力－系統瞬時尖峰負載(瞬間值)）÷系統瞬時尖峰負載(瞬間值)×100%
#### 系統運轉淨尖峰供電能力
系統運轉淨尖峰供電能力：扣除歲修(機組大修)、小修(機組檢修)及故障機組容量、火力機組環保限制、輔機故障、氣溫變化、水力考慮水位、水文、灌溉及溢流
### 110 備轉表
![](https://i.imgur.com/R8Qnjo1.png)
1. 發現1-4月備轉容量較穩定 約再2500-3500間
2. 而順時尖峰負載則是呈現似二次函數相接
### 111 備轉表
![](https://i.imgur.com/xVkcBi9.png)
1. 111年根本災難 備轉容量根本超參差的
### 統整

#### 瞬時尖峰負載
* 今年周尖峰負載
![](https://i.imgur.com/aQSwY73.png)
1. 發現  local lowest point 多為周末，推測應該是周末工業休息。
2. 發現 local highest point 大多為星期三、四
* 去年至今年2月比例圖
![](https://i.imgur.com/R0pULMW.png)

#### 供電能力
* 今年周供電圖
![](https://i.imgur.com/w94vvAZ.png)
* 去年至今年2月比例圖
![](https://i.imgur.com/OJfmvul.png)

#### 備轉容量
今年周備轉容量
![](https://i.imgur.com/HpsVSxb.png)
1. 找不太到關鍵點，聽天命了。
2. 1-2月的部分差距還算可接受。
* 去年至今年2月比例圖
![](https://i.imgur.com/AS5DlGF.png)
今年的參差度相較於去年差很多


## 影響供電來源
工業用電跟民生用電大約分別佔上55%及45%
以氣溫來說確實會影響些，但系統運轉淨尖峰能力，我們這裡卻很難找到方式預估。
## 如何預估
所以最後還是先抓系統運轉淨尖峰能力的平均基準點，自行想像4月份可能之溫度，再以星期
幾去調整尖峰負載參數，最後得出備轉容量的預估值。

## 使用資料
* 本年度每日尖峰備轉容量率
    * 用於主要估計之因素
* 台灣電力公司_過去電力供需資訊
    * 利用過去資訊作為調整參數
## 整理Feature
### 主要整理為六個欄位
1. 日期
2. 星期
3. 淨尖峰供電能力(MW)
4. 尖峰負載(MW)
5. 備轉容量(MW)
6. 備轉容量率(%)

### 簡單預測
1. 將前幾天的淨尖峰供電能力與去年淨尖峰供電能力依比例校正。
2. 若時間為周末則將前一天之尖峰負載(MW)降載，若為周間則依週三為基準點分點。
3. 最後加入決定命運的random對備轉容量0.8~1.2 做調整。

