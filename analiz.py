import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib import rcParams

rcParams['font.family'] = 'DejaVu Sans'

with open('cat_breeds.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data['cat_breeds'])

# График 1: Распределение пород по размерам
plt.figure(figsize=(10, 6))
size_counts = df['size'].value_counts()
plt.bar(size_counts.index, size_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.title('**Распределение пород кошек по размерам**', fontsize=16, fontweight='bold')
plt.xlabel('Размер', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(size_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 2: Анализ уровня интеллекта пород
plt.figure(figsize=(12, 8))
intelligence_data = df['intelligence'].value_counts().sort_index()
plt.bar(intelligence_data.index.astype(str), intelligence_data.values,
        color=plt.cm.viridis(np.linspace(0, 1, len(intelligence_data))))
plt.title('**Распределение пород по уровню интеллекта**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень интеллекта (по 10-балльной шкале)', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(intelligence_data.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 3: Дружелюбность к детям
plt.figure(figsize=(8, 6))
child_friendly = df['child_friendly'].value_counts().sort_index()
plt.bar(child_friendly.index.astype(str), child_friendly.values, color='lightcoral')
plt.title('**Дружелюбность к детям**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень дружелюбности', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(child_friendly.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 4: Дружелюбность к другим животным
plt.figure(figsize=(8, 6))
pet_friendly = df['pet_friendly'].value_counts().sort_index()
plt.bar(pet_friendly.index.astype(str), pet_friendly.values, color='lightseagreen')
plt.title('**Дружелюбность к другим животным**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень дружелюбности', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(pet_friendly.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 5: Анализ уровня ухода за шерстью
plt.figure(figsize=(10, 6))
grooming_data = df['grooming'].value_counts().sort_index()
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700', '#FF69B4']
plt.pie(grooming_data.values, labels=grooming_data.index, autopct='%1.1f%%',
        colors=colors, startangle=90)
plt.title('**Распределение по уровню ухода за шерстью**', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# График 6: Уровень активности пород
plt.figure(figsize=(8, 6))
activity_levels = df['activity_level'].value_counts()
plt.bar(activity_levels.index, activity_levels.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.title('**Уровень активности пород**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень активности', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(activity_levels.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 7: Потребность во внимании
plt.figure(figsize=(8, 6))
attention_data = df['attention_need'].value_counts().sort_index()
plt.bar(attention_data.index.astype(str), attention_data.values, color='orange')
plt.title('**Потребность во внимании**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень потребности во внимании', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(attention_data.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 8: Уровень здоровья пород
plt.figure(figsize=(8, 6))
health_data = df['health'].value_counts().sort_index()
plt.bar(health_data.index.astype(str), health_data.values, color='lightgreen')
plt.title('**Уровень здоровья пород**', fontsize=16, fontweight='bold')
plt.xlabel('Уровень здоровья', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(health_data.values):
    plt.text(i, v + 0.3, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 9: Уровень линьки
plt.figure(figsize=(8, 6))
shedding_data = df['shedding'].value_counts()
plt.pie(shedding_data.values, labels=shedding_data.index, autopct='%1.1f%%',
        colors=['#FF9999', '#66B2FF', '#99FF99'])
plt.title('**Уровень линьки пород**', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# График 10: Анализ продолжительности жизни
plt.figure(figsize=(12, 6))
# Извлекаем числовое значение продолжительности жизни
def extract_lifespan(lifespan_str):
    try:
        return int(lifespan_str.split('-')[0])
    except:
        return 12

df['lifespan_min'] = df['lifespan'].apply(extract_lifespan)

plt.hist(df['lifespan_min'], bins=8, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('**Распределение минимальной продолжительности жизни**', fontsize=16, fontweight='bold')
plt.xlabel('Продолжительность жизни (лет)', fontsize=12)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# График 11: Популярные характеристики пород
plt.figure(figsize=(10, 6))
high_intelligence = len(df[df['intelligence'] >= 8])
high_child_friendly = len(df[df['child_friendly'] >= 4])
low_grooming = len(df[df['grooming'] <= 2])
good_health = len(df[df['health'] >= 4])

demand_params = ['Высокий интеллект', 'Дружелюбность к детям', 'Низкий уход', 'Хорошее здоровье']
demand_values = [high_intelligence, high_child_friendly, low_grooming, good_health]

plt.bar(demand_params, demand_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD700'])
plt.title('**Популярные характеристики пород**', fontsize=16, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Количество пород', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(demand_values):
    plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# График 12: Потенциальная аудитории бота
plt.figure(figsize=(8, 8))
audience_segments = ['Семьи с детьми', 'Занятые люди', 'Аллергики', 'Опытные владельцы']
segment_sizes = [65, 45, 30, 25]
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700']

plt.pie(segment_sizes, labels=audience_segments, autopct='%1.1f%%', colors=colors)
plt.title('**Потенциальная аудитория бота (%)**', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# График 13: Прогноз роста пользователей и дохода
fig, ax1 = plt.subplots(figsize=(10, 6))

months = ['Месяц 1', 'Месяц 3', 'Месяц 6', 'Месяц 12']
users = [100, 500, 1500, 5000]
revenue = [0, 2500, 15000, 75000]

ax1.plot(months, users, marker='o', linewidth=2, markersize=8, color='green', label='Пользователи')
ax1.set_title('**Прогноз роста пользователей и дохода**', fontsize=16, fontweight='bold')
ax1.set_ylabel('Количество пользователей', color='green')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='y', labelcolor='green')

ax2 = ax1.twinx()
ax2.plot(months, revenue, marker='s', linewidth=2, markersize=8, color='red', linestyle='--', label='Доход')
ax2.set_ylabel('Доход (руб)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.tight_layout()
plt.show()

# График 14: Социальная значимость проекта
plt.figure(figsize=(10, 6))
impact_areas = ['Уменьшение\nотказов', 'Повышение\nосведомленности', 'Улучшение\nсовместимости', 'Поддержка\nпитомников']
impact_scores = [85, 75, 90, 70]

plt.barh(impact_areas, impact_scores, color=plt.cm.Set3(np.linspace(0, 1, 4)))
plt.title('**Социальная значимость проекта**', fontsize=16, fontweight='bold')
plt.xlabel('Оценка влияния (%)', fontsize=12)
plt.grid(axis='x', alpha=0.3)
for i, v in enumerate(impact_scores):
    plt.text(v + 1, i, str(v) + '%', va='center', fontweight='bold')
plt.tight_layout()
plt.show()
