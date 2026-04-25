# Sentinel-значение для «нет данных по частоте коммитов».
# Используется вместо магического числа 666 во всех местах проекта:
#   - C_generation_fake_users.py  (_absolute_zero, _low_values)
#   - C_ProfileAssessment.py      (_apply_zero_constraints)
#   - C_UserRepo.py               (commits_frequency_in_day fallback)
NO_FREQUENCY_SENTINEL: float = 666.0