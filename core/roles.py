from rolepermissions.roles import AbstractUserRole


class Fornecedor(AbstractUserRole):
    available_permissions = {
        'view_necessary_food': True,
        'add_food_provided': True,
    }
