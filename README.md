# Tasks for tetrika

## Task 1
<p>Решен через бинарный поиск. Сложность алгоритма O(log n)</p>
<p>to run use -> ``` python task1.py ``` or ``` python3 task1.py ```</p>

## Task 2
<p> Парсим в одном потоке, если __name__ == '__main__'.
Для запуска выполните </p>
<p>``` python task2.py [LETTER] ``` где LETTER (опционально) - буква, на которой стоит остановится парсить,
по умолчанию значение A - англ. алфавит. Сама LETTER не будет включена. </p>
<p> Прошу учесть, что передавать скрипту надо только одну букву. Фича сделана для экономии только
Вашего времени (что бы урезать кол-во страниц, подлежащих парсингу) при проверке задания,
по этому там никаких проверок на то, что вводит пользователь</p>

<p>p.s. Я писал скрипт исходя из того, что Wiki отдает список животных в алфавитном порядке,
но оказалось, что в результат подмешивается некая пиявка с названием 'Helobdella nununununojensis'. 
Просто ислючил её из выдачи hotfix'ом - проверкой ключей словаря по регулярке перед выполенением print()</p>
<p>p.s.s. Я использовал словарь для хранения названий животных,
по этому выдача будет несортированная (в условии не сказано про сортировку в выдаче)</p>

## Task 3
