import cabina


class Config(cabina.Config, cabina.Section):
    GOLDEN_API_URL = cabina.env.str('GOLDEN_API_HOST')
    TESTING_API_URL = cabina.env.str('TESTING_API_HOST')
