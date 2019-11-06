from .. import checks

ERR_MSG = "database failed"


def bad_database_check(*args, **kwargs):
    raise checks.HealthcheckFailure(ERR_MSG)
