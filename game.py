import random

def guess_number_game():
    """
    一个简单的猜数字游戏
    计算机随机生成1-100之间的数字，玩家需要猜出这个数字
    """
    print("=" * 50)
    print("欢迎来到猜数字游戏！")
    print("=" * 50)
    print()
    
    # 计算机随机生成1-100之间的数字
    secret_number = random.randint(1, 100)
    attempts = 0
    guessed = False
    
    print("我已经想好了一个1-100之间的数字")
    print("你有机会猜出这个数字！")
    print()
    
    while not guessed:
        try:
            # 获取玩家输入
            guess = int(input("请输入你的猜测 (1-100): "))
            
            # 检查输入范围
            if guess < 1 or guess > 100:
                print("❌ 请输入1-100之间的数字!")
                continue
            
            attempts += 1
            
            # 比较猜测和秘密数字
            if guess < secret_number:
                print(f"📈 太小了！再试试看...")
            elif guess > secret_number:
                print(f"📉 太大了！再试试看...")
            else:
                guessed = True
                print()
                print("=" * 50)
                print("🎉 恭喜你猜对了！")
                print(f"秘密数字就是：{secret_number}")
                print(f"你用了 {attempts} 次尝试")
                print("=" * 50)
                
                # 根据尝试次数给出评价
                if attempts <= 5:
                    print("🏆 你真是个天才！")
                elif attempts <= 10:
                    print("👍 不错！你的直觉很准！")
                else:
                    print("💪 坚持不懈，最终成功！")
        
        except ValueError:
            print("❌ 无效输入！请输入一个数字")
        
        print()

def main():
    """主程序"""
    while True:
        guess_number_game()
        
        # 询问是否继续游戏
        play_again = input("想再玩一局吗？(是/否): ").strip().lower()
        if play_again not in ['是', 'yes', 'y']:
            print()
            print("感谢游玩！再见！👋")
            break
        print()

if __name__ == "__main__":
    main()
