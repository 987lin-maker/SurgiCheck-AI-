# SurgiCheck-AI
# SurgiCheck - 手術器械AI自動盤點系統 🏥✂️

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-UI_Completed_|_Model_WIP-orange.svg)
![Platform](https://img.shields.io/badge/Edge_AI-NVIDIA_Jetson-76B900.svg)

**SurgiCheck** 是一款專為臨床供應中心（CSSD）設計的智慧醫療解決方案。透過導入電腦視覺（Computer Vision）與邊緣運算（Edge Computing），旨在解決傳統手術器械盤點耗時、標籤易脫落及人為疏失等痛點，提升醫療流程的安全與效率。

---

## 🌟 核心功能 (Features)

1. **安全認證登入系統**
   * 具備臨床資訊安全考量的分級權限管控。
2. **直覺式器械包選擇**
   * 採用卡片式 UI 設計，提供如「一般外科基礎包」、「骨科基礎器械包」等快速選單。
   * 預防防呆機制，確保選擇目標後才能啟動邊緣主機串流。
3. **即時 AI 盤點工作台 (待開發中)**
   * **左側視角**：即時顯示相機影像串流與 AI 辨識定界框（Bounding Box）。
   * **右側視角**：自動化結構清單，實時對比「應有數量」與「AI 辨識數」。
   * **狀態監控**：即時顯示邊緣主機與設備的連線狀態。

---

## 🛠 技術架構 (Tech Stack)

### 目前已實作 (前端介面)
* **語言**: Python 3
* **GUI 框架**: Tkinter (純原生打造現代化無邊框風格)

### 團隊待開發中 (AI 模型與邊緣硬體)
* **AI 辨識模型**: 預計採用 **YOLOv8 / YOLO11** 架構進行手術器械特徵萃取與物件偵測。
* **邊緣運算平台**: 預計部署於 **NVIDIA Jetson Orin Nano**，確保資料不出院內的隱私性與低延遲。
* **視覺感知層**: 預計使用C310 logitech 免驅動 HD攝影機 720P 網路鏡頭，處理反光與金屬堆疊問題。

---

## 🚀 系統安裝與執行方式

### 1. 環境需求
請確保您的電腦已安裝 Python 3.8 或以上版本。

### 2. 複製專案
git clone [https://github.com/您的帳號/SurgiCheck.git](https://github.com/您的帳號/SurgiCheck.git)
cd SurgiCheck

### 3. 安裝相依套件
介面主要使用內建庫，但需安裝 Pillow 處理圖片資源：
pip install pillow

### 4. 準備圖片資源
請確保專案根目錄下有一張名為 logo.png 的圖片（建議尺寸為正方形，如 512x512），系統會自動將其縮放渲染至介面中。若無圖片，系統將自動以備用 Emoji 顯示，不會影響執行。

### 5. 啟動系統
python app.py
🔑 預設測試帳號 (Demo Credentials)
為了方便進行 UI 流程測試，系統內建了一組 Root 測試帳號：

員工編號: SurgiCheck

安全密碼: aiot0721

(註：正式上線版本將介接院內資料庫進行驗證，不保留硬編碼密碼)

🗺 開發藍圖 (Roadmap)

[ ] Phase 1: 建構手術器械影像資料集（Data Collection & Augmentation）。

[ ] Phase 2: 訓練 YOLO 辨識模型並進行超參數優化。

[ ] Phase 3: 將模型轉換為 TensorRT 格式，部署至 NVIDIA Jetson Orin Nano。

[ ] Phase 4: 整合 C310 網路鏡頭串流至 Tkinter 介面並輸出即時盤點報表。
