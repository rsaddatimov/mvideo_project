class PropertyHacker(type):
    """
    Метакласс для удобного переопределения property
    -----------------------------------------------
    Принцип работы (упрощенно): пусть в классе есть property с названием <name>.
    При инициализации класса (а также всех его наследников) в нем ищутся методы
    get_<name> + set_<name>, и устанавливаются в качестве геттера и сеттера
    соответственно. Чтобы переопределить геттер или сеттер в дочернем классе,
    достаточно просто создать соответствующий get_* или set_* метод, а обо всем
    остальном позаботится данный метакласс. И не нужно никаких конченных декораторов.
    """

    def __new__(mcs, name, bases, attrs):
        # Временно создаем новый класс - он нужен для того,
        # чтобы получить доступ к родительским атрибутам
        new = super().__new__(mcs, name, bases, attrs)

        # В all будут *все* атрибуты класса, включая родительские
        # Оверрайды учитываются благодаря .update()
        all = {k: getattr(new, k) for k in dir(new)}
        all.update(attrs)

        for name, value in all.items():
            # Проверяем все найденные property
            if isinstance(value, property):
                # Вытаскиваем предполагаемый геттер + сеттер,
                # а также оригинальный docstring
                getter = all.get('get_' + name)
                setter = all.get('set_' + name)
                doc = value.__doc__

                # Проверяем, а нужно ли вообще пересоздавать property
                if value.fget != getter or value.fset != setter:
                    attrs[name] = property(getter, setter, doc=doc)

        # Возвращаем окончательный вариант класса
        return super().__new__(mcs, name, bases, attrs)