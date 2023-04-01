# 110-1-goodmorning-picture-linobot
# Demo Video:
  https://www.youtube.com/watch?v=vnAm8nn3DA4
  
# introduce:
這是一個linebot，讓長輩能一鍵快速生成長輩圖。使用蓮花的dataset訓練蓮花圖片生成模型，以及用自然語言處理生成祝福句子，將模型生成的蓮花圖片與NLP文字合成一張AI長輩圖。

<img width="200" alt="image" src="https://user-images.githubusercontent.com/32382354/229274678-3be40b57-68cb-45b4-99de-b63659b70e1f.png">



# generate picture part:
  - Projected GAN
  - Epoch : 300
  - Dataset :Oxford-102-flower from Kaggle(train on lotus flower only)
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/32382354/229274936-560f15c4-8dd3-49ca-9f08-076d400cec1b.png">


# NLP part:
  - Dataset:Wikipedia Chinese datasets(traditional)
  - preprocess: openCC + Jieba 
  - trained by GENSIM

# generate blessing sentence part:
  - dataset: Collect commonly used phrases for blessing sentence from the internet.
  - generate flow : articut + our NLP model
  <img width="300" alt="image" src="https://user-images.githubusercontent.com/32382354/229275311-55854480-e48f-49b2-bd2e-394000f4a145.png">

# linebot part:
  -   3 functions:
  >1.  Enter text and pair it with the lotus flower image we generate.
  >2.  Upload an image and pair it with the blessing sentence we generate.
  >3.  Enter text and upload an image. Both are paired with what we generate.
