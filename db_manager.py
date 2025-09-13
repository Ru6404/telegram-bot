import sqlite3

def add_test_data():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    
    # Добавляем тестовых клиентов
    test_clients = [
        (1001, 'Иван Иванов', '@ivanov'),
        (1002, 'Мария Петрова', '@maria'),
        (1003, 'Алексей Сидоров', '@alex')
    ]
    
    for client in test_clients:
        cursor.execute('INSERT OR IGNORE INTO clients (telegram_id, name, username) VALUES (?, ?, ?)', client)
    
    # Добавляем тестовые задачи
    cursor.execute('SELECT id FROM clients WHERE telegram_id = 1001')
    client_id = cursor.fetchone()[0]
    
    test_tasks = [
        (client_id, 'Разработка сайта', 'Создание корпоративного сайта', 'высокий'),
        (client_id, 'Настройка SEO', 'Оптимизация сайта для поиска', 'средний'),
        (client_id, 'Консультация', 'Обсуждение нового проекта', 'низкий')
    ]
    
    for task in test_tasks:
        cursor.execute('INSERT INTO tasks (client_id, title, description, priority) VALUES (?, ?, ?, ?)', task)
    
    conn.commit()
    conn.close()
    print("✅ Тестовые данные добавлены")

if __name__ == '__main__':
    add_test_data()
