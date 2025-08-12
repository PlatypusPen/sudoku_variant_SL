import yaml
import re
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def parse_line(s):
    # 去除空格
    s = s.replace(" ", "")
    
    # 匹配所有 "(x,y)" 形式的坐标
    pattern = r"\((\d),(\d)\)"
    matches = re.findall(pattern, s)
    
    # 转为整型坐标列表
    node_list = [(int(x), int(y)) for x, y in matches]
    coord_list = [node_list[0]]
    # 检查是否满足所有约束
    for i in range(len(node_list) - 1):
        x1, y1 = node_list[i]
        x2, y2 = node_list[i + 1]
        
        # 坐标不能相同
        if x1 == x2 and y1 == y2:
            raise ValueError(f"第 {i+1} 和 {i+2} 个坐标相同：({x1},{y1})")
        
        # 检查是否在横线、竖线或斜线（对角线）
        dx, dy = x2 - x1, y2 - y1
        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            raise ValueError(f"第 {i+1} 和 {i+2} 个坐标不在横/竖/斜线上：({x1},{y1}) 到 ({x2},{y2})")
        sx = sign(dx)
        sy = sign(dy)
        for stp in range(1, max(abs(dx), abs(dy)) + 1):
            coord_list.append((x1 + sx * stp, y1 + sy * stp))
        
    return coord_list

with open('test.yaml', 'r') as file:
    data = yaml.safe_load(file)
    print(data)
    l = parse_line(data['german_whisper'][0])
    print(l)