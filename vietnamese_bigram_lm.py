import os
import tarfile
import urllib.request
import re
import math
import random
from collections import defaultdict, Counter

CORPUS_URL = "https://downloads.wortschatz-leipzig.de/corpora/vie_news_2020_10K.tar.gz"
CORPUS_ARCHIVE = "vie_news_2020_10K.tar.gz"
CORPUS_TXT = "vie_news_2020_10K-sentences.txt"

def download_and_extract_corpus():
    """Tải và giải nén corpus từ Leipzig."""
    if not os.path.exists(CORPUS_TXT):
        if not os.path.exists(CORPUS_ARCHIVE):
            print(f"Đang tải dữ liệu từ {CORPUS_URL}...")
            urllib.request.urlretrieve(CORPUS_URL, CORPUS_ARCHIVE)
            print("Đã tải xong.")
        print("Đang giải nén tập tin...")
        with tarfile.open(CORPUS_ARCHIVE, "r:gz") as tar:
            for member in tar.getmembers():
                if member.name.endswith("sentences.txt"):
                    member.name = CORPUS_TXT  # Ghi đè đường dẫn để giải nén ra thư mục hiện tại
                    tar.extract(member)
        print("Dữ liệu đã sẵn sàng.")
    else:
        print("Đã tìm thấy tập dữ liệu cục bộ.")

def load_corpus(file_path):
    """Đọc dữ liệu từ file corpus."""
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                sentences.append(parts[1])
            else:
                sentences.append(line.strip())
    return sentences

def preprocess(text):
    """Tiền xử lý văn bản: chuyển chữ thường, loại bỏ dấu câu, tách âm tiết."""
    text = str(text).lower()
    # Loại bỏ các ký tự không phải chữ, số hoặc khoảng trắng
    text = re.sub(r'[^\w\s]', '', text)
    # Tách thành các âm tiết
    syllables = text.split()
    return syllables

class BigramLM:
    def __init__(self):
        self.unigram_counts = Counter()
        self.bigram_counts = defaultdict(Counter)
        self.vocab = set()
        self.vocab_size = 0
        
    def train(self, sentences):
        """Huấn luyện mô hình N-gram trên danh sách các câu."""
        print(f"Đang huấn luyện mô hình với {len(sentences)} câu...")
        for sentence in sentences:
            # Thêm token bắt đầu <s> và kết thúc </s>
            syllables = ['<s>'] + preprocess(sentence) + ['</s>']
            self.vocab.update(syllables)
            
            for i in range(len(syllables)):
                self.unigram_counts[syllables[i]] += 1
                if i < len(syllables) - 1:
                    self.bigram_counts[syllables[i]][syllables[i+1]] += 1
                    
        self.vocab_size = len(self.vocab)
        print(f"Đã huấn luyện xong! Kích thước từ vựng (vocab_size): {self.vocab_size}")
        
    def get_prob(self, w1, w2):
        """Tính P(w2 | w1) với Add-1 (Laplace) Smoothing."""
        # P(w2|w1) = (C(w1, w2) + 1) / (C(w1) + V)
        count_w1_w2 = self.bigram_counts[w1][w2]
        count_w1 = self.unigram_counts[w1]
        
        prob = (count_w1_w2 + 1) / (count_w1 + self.vocab_size)
        return prob
        
    def calculate_sentence_prob(self, sentence):
        """Tính và in ra xác suất của một câu hoàn chỉnh."""
        syllables = ['<s>'] + preprocess(sentence) + ['</s>']
        print(f"\n[PHÂN TÍCH XÁC SUẤT]")
        print(f"Câu gốc: '{sentence}'")
        print(f"Tokens: {syllables}")
        
        log_prob = 0.0
        for i in range(len(syllables) - 1):
            w1 = syllables[i]
            w2 = syllables[i+1]
            p = self.get_prob(w1, w2)
            log_prob += math.log10(p)
            print(f"  P({w2:<10} | {w1:<10}) = {p:.6e} (log10: {math.log10(p):.4f}) -> [C({w1},{w2})={self.bigram_counts[w1][w2]}, C({w1})={self.unigram_counts[w1]}]")
            
        actual_prob = math.pow(10, log_prob)
        print(f"-> Tổng xác suất (Log10): {log_prob:.4f}")
        print(f"-> Tổng xác suất: {actual_prob:.6e}")
        return actual_prob

    def generate_sentence(self, max_len=20):
        """Sinh ra một câu ngẫu nhiên dựa trên các bigram đã học (Không sinh random noise từ smoothing)."""
        sentence = []
        current_word = '<s>'
        
        while len(sentence) < max_len:
            # Chọn các từ tiếp theo dựa trên các bigram ĐÃ QUAN SÁT để câu có nghĩa hơn
            observed_counts = self.bigram_counts.get(current_word, {})
            
            if not observed_counts: # Đường cụt
                break
                
            words = list(observed_counts.keys())
            counts = list(observed_counts.values())
            
            # Tính phân phối xác suất từ số đếm (trọng số)
            total_count = sum(counts)
            probs = [c / total_count for c in counts]
            
            # Lấy ngẫu nhiên theo phân phối xác suất
            next_word = random.choices(words, weights=probs, k=1)[0]
            
            if next_word == '</s>':
                break
                
            if next_word != '<s>':
                sentence.append(next_word)
                
            current_word = next_word
            
        # Nối các âm tiết lại và viết hoa chữ cái đầu
        generated_text = " ".join(sentence)
        if generated_text:
            generated_text = generated_text[0].upper() + generated_text[1:]
        return generated_text

def main():
    print("="*60)
    print("MÔ HÌNH NGÔN NGỮ BIGRAM TIẾNG VIỆT MỨC ÂM TIẾT")
    print("="*60)
    
    # 1. Tải corpus
    download_and_extract_corpus()
    
    # 2. Đọc corpus
    sentences = load_corpus(CORPUS_TXT)
    
    # 3. Khởi tạo và huấn luyện mô hình
    model = BigramLM()
    model.train(sentences)
    
    # 4. Tính xác suất một đoạn câu mẫu theo yêu cầu
    test_sentence = "Hôm nay trời đẹp lắm"
    model.calculate_sentence_prob(test_sentence)
    
    # 5. Sinh một số câu từ mô hình
    print(f"\n[SINH CÂU TỰ ĐỘNG TỪ MÔ HÌNH]")
    for i in range(5):
        gen_sent = model.generate_sentence()
        print(f"Câu {i+1}: {gen_sent}")
        
    print("\nQuá trình hoàn tất.")

if __name__ == "__main__":
    main()
