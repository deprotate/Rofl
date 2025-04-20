import json
import random
import re
from collections import defaultdict
from typing import Dict, List, Any


def generateTask(prompt: str, dataPath: str) -> Dict[str, Any]:
    generator = TaskGenerator(dataPath)
    return generator.generate(prompt)


class TaskGenerator:
    def __init__(self, dataPath: str) -> None:
        with open(dataPath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)['examples']

        self.domainData = self.buildDomainData()
        self.templates = [
            "Оптимизация {process} в {domain}",
            "Анализ {aspect} в {domain}",
            "Разработка {solution} для {problem}",
            "Исследование {subject} в условиях {conditions}",
            "Сравнение {item1} и {item2} в {domain}"
        ]

    def buildDomainData(self) -> Dict[str, Dict[str, set]]:
        domains = defaultdict(lambda: {
            'processes': set(), 'domains': set(), 'aspects': set(),
            'solutions': set(), 'problems': set(), 'subjects': set(),
            'conditions': set(), 'items': set()
        })

        domainKeywords = {
            'ai': ['искусственн', 'нейросет', 'машинн', 'алгоритм'],
            'economics': ['экономик', 'финанс', 'предприят', 'рынок'],
            'ecology': ['экологи', 'природ', 'эколог', 'окружающ']
        }

        for item in self.data:
            currentDomain = 'other'
            text = item['prompt'].lower() + ' ' + item['output']['topic'].lower()
            for domain, keywords in domainKeywords.items():
                if any(kw in text for kw in keywords):
                    currentDomain = domain
                    break

            topic = item['output']['topic']
            domains[currentDomain]['domains'].update(re.findall(r'\b[\w-]+\b', topic))

            for crit in item['output']['criteria']:
                words = re.findall(r'\b[\w-]+\b', crit.lower())
                domains[currentDomain]['processes'].update(words)
                domains[currentDomain]['aspects'].update(words)
                domains[currentDomain]['problems'].update(words)

        return domains

    def getDomainTerms(self, domain: str) -> Dict[str, List[str]]:
        baseTerms = {
            'ai': {
                'process': ['обучение моделей', 'обработка данных', 'распознавание образов'],
                'domain': ['искусственный интеллект', 'машинное обучение', 'компьютерное зрение'],
                'aspect': ['эффективность алгоритмов', 'точность предсказаний', 'скорость обучения'],
                'solution': ['новый алгоритм', 'оптимизированная модель', 'улучшенная архитектура'],
                'problem': ['переобучение моделей', 'нехватка данных', 'интерпретируемость результатов'],
                'subject': ['глубокие нейронные сети', 'методы обучения', 'архитектуры моделей'],
                'conditions': ['больших данных', 'ограниченных ресурсов', 'реального времени'],
                'item': ['сверточные сети', 'рекуррентные сети', 'трансформеры']
            },
            'economics': {
                'process': ['финансовое планирование', 'управление ресурсами', 'оптимизация затрат'],
                'domain': ['корпоративные финансы', 'экономика предприятия', 'рыночная экономика'],
                'aspect': ['финансовая устойчивость', 'рентабельность', 'конкурентные преимущества'],
                'solution': ['финансовая стратегия', 'модель оптимизации', 'методика оценки'],
                'problem': ['управление рисками', 'повышение эффективности', 'снижение издержек'],
                'subject': ['инвестиционные стратегии', 'финансовые показатели', 'рыночные тенденции'],
                'conditions': ['экономического кризиса', 'глобализации', 'цифровизации'],
                'item': ['традиционные методы', 'инновационные подходы', 'зарубежный опыт']
            },
            'ecology': {
                'process': ['очистка сточных вод', 'управление отходами', 'мониторинг загрязнений'],
                'domain': ['экологический менеджмент', 'охрана окружающей среды', 'устойчивое развитие'],
                'aspect': ['эффективность очистки', 'уровень загрязнения', 'биоразнообразие'],
                'solution': ['программа мониторинга', 'система переработки', 'методика восстановления'],
                'problem': ['загрязнение атмосферы', 'деградация почв', 'сокращение биоразнообразия'],
                'subject': ['экосистемы городов', 'климатические изменения', 'природные ресурсы'],
                'conditions': ['антропогенного воздействия', 'изменения климата', 'урбанизации'],
                'item': ['традиционные методы', 'инновационные технологии', 'зарубежный опыт']
            },
            'other': {
                'process': ['управленческие процессы', 'производственные циклы', 'технологические операции'],
                'domain': ['предметная область', 'актуальная сфера', 'исследуемое направление'],
                'aspect': ['основные характеристики', 'ключевые параметры', 'важные факторы'],
                'solution': ['концептуальное решение', 'практическая методика', 'эффективный алгоритм'],
                'problem': ['актуальная проблема', 'типовые затруднения', 'практические вопросы'],
                'subject': ['основной объект', 'ключевой элемент', 'центральный вопрос'],
                'conditions': ['современных реалий', 'изменяющейся среды', 'конкретных обстоятельств'],
                'item': ['разные подходы', 'альтернативные методы', 'сравнимые объекты']
            }
        }

        terms = baseTerms.get(domain, baseTerms['other'])
        for key in terms:
            if key in self.domainData[domain]:
                terms[key].extend(list(self.domainData[domain][key]))
        return terms

    def generate(self, prompt: str) -> Dict[str, Any]:
        domain = 'other'
        promptLower = prompt.lower()
        if any(kw in promptLower for kw in ['искусственн', 'нейросет', 'машинн', 'алгоритм']):
            domain = 'ai'
        elif any(kw in promptLower for kw in ['экономик', 'финанс', 'предприят', 'рынок']):
            domain = 'economics'
        elif any(kw in promptLower for kw in ['экологи', 'природ', 'эколог', 'окружающ']):
            domain = 'ecology'

        terms = self.getDomainTerms(domain)
        template = random.choice(self.templates)
        placeholders = re.findall(r'\{(\w+)\}', template)

        replacements = {}
        for ph in placeholders:
            replacements[ph] = random.choice(terms[ph]) if ph in terms and terms[ph] else 'исследуемого объекта'

        topic = template.format(**replacements).capitalize()

        criteriaOptions = [
            f"Анализ {random.choice(terms['aspect'])}",
            f"Исследование {random.choice(terms['process'])}",
            f"Разработка {random.choice(terms['solution'])}",
            f"Оценка {random.choice(terms['aspect'])}",
            f"Сравнение {random.choice(terms['item'])}"
        ]
        criteria = random.sample(criteriaOptions, 3)

        isDiploma = any(w in promptLower for w in ['диплом', 'выпускн'])
        deadline = f"{random.randint(4, 6)} месяца" if isDiploma else f"{random.randint(2, 4)} {'недели' if random.random() > 0.5 else 'месяца'}"

        return {
            "topic": topic,
            "criteria": criteria,
            "deadline": deadline
        }


result = generateTask("Диплом по искусственному интеллекту", "dataset.json")
print(json.dumps(result, indent=2, ensure_ascii=False))
