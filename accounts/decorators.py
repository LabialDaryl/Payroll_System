from django.contrib.auth.decorators import user_passes_test


def group_required(group_name):
    def in_groups(u):
        if u.is_authenticated:
            return u.groups.filter(name=group_name).exists() or u.is_superuser
        return False
    return user_passes_test(in_groups)
