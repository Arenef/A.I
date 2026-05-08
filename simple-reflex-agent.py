import random
import time

# ==========================================
# 1. ĐỊNH NGHĨA TÁC TỬ
# ==========================================
class StrictlyStructuredRandomAgent:
    def __init__(self):
        # persistent: rules
        self.rules = {
            'ĐÃ_TỚI_ĐÍCH': 'DỪNG LẠI',
            'CHƯA_TỚI_ĐÍCH': 'ĐI NGẪU NHIÊN'
        }
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.valid_actions = ['LÊN', 'XUỐNG', 'TRÁI', 'PHẢI']

    def interpret_input(self, percept):
        # state <- INTERPRET-INPUT(percept)
        if percept == self.goal_state:
            return 'ĐÃ_TỚI_ĐÍCH'
        else:
            return 'CHƯA_TỚI_ĐÍCH'

    def rule_match(self, state, rules):
        # rule <- RULE-MATCH(state, rules)
        loai_hanh_dong = rules.get(state)
        
        if loai_hanh_dong == 'DỪNG LẠI':
            return 'STOP'
        elif loai_hanh_dong == 'ĐI NGẪU NHIÊN':
            return random.choice(self.valid_actions)

    def act(self, percept):
        # function SIMPLE-REFLEX-AGENT(percept)
        state = self.interpret_input(percept)
        action = self.rule_match(state, self.rules)
        return action

# ==========================================
# 2. HÀM MÔI TRƯỜNG & HIỂN THỊ
# ==========================================
def in_ban_co(state):
    for i in range(0, 9, 3):
        row = ["_" if x == 0 else str(x) for x in state[i:i+3]]
        print(f" {row[0]} | {row[1]} | {row[2]} ")
    print("-" * 11)

def cap_nhat_moi_truong(state, action):
    state_list = list(state)
    idx = state_list.index(0)
    r, c = divmod(idx, 3)
    
    new_r, new_c = r, c
    if action == 'LÊN': new_r -= 1
    elif action == 'XUỐNG': new_r += 1
    elif action == 'TRÁI': new_c -= 1
    elif action == 'PHẢI': new_c += 1
    
    # Nếu nước đi không bị văng ra khỏi bàn cờ
    if 0 <= new_r < 3 and 0 <= new_c < 3:
        new_idx = new_r * 3 + new_c
        state_list[idx], state_list[new_idx] = state_list[new_idx], state_list[idx]
        return tuple(state_list), True
    return state, False

# ==========================================
# 3. CHẠY MÔ PHỎNG 
# ==========================================
if __name__ == "__main__":
    agent = StrictlyStructuredRandomAgent()
    
    # Đặt một trạng thái dễ để Agent nhanh tìm được đích
    # Trạng thái này chỉ cần đẩy số 8 sang trái là xong
    ban_co_hien_tai = (1, 2, 3, 4, 5, 6, 7, 0, 8) 
    
    print("=== MỤC TIÊU CẦN ĐẠT ===")
    in_ban_co(agent.goal_state)
    print("Bắt đầu mô phỏng...")
    time.sleep(2)
    
    buoc = 0
    while True:
        buoc += 1
        print(f"\n[BƯỚC {buoc}]")
        in_ban_co(ban_co_hien_tai)
        
        # Tác tử phân tích và hành động
        hanh_dong = agent.act(ban_co_hien_tai)
        trang_thai = agent.interpret_input(ban_co_hien_tai)
        
        print(f"-> Trạng thái: {trang_thai}")
        print(f"-> Hành động: {hanh_dong}")
        
        if hanh_dong == 'STOP':
            print(f"THÀNH CÔNG! Agent đã hoàn thành trò chơi sau {buoc-1} bước.")
            break
            
        # Môi trường cập nhật
        ban_co_moi, hop_le = cap_nhat_moi_truong(ban_co_hien_tai, hanh_dong)
        
        if hop_le:
            ban_co_hien_tai = ban_co_moi
        else:
            print("-> (Cố gắng đi vào tường, môi trường giữ nguyên vị trí)")
            
        time.sleep(0.3) # Gián đoạn 0.3 giây để bạn kịp xem
        
        # Ngắt vòng lặp nếu nó chạy quá lâu
        if buoc >= 100:
            print("THẤT BẠI: Đã quá 100 bước, Agent không giải được rồi!")
            break