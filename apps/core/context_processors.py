def site_settings(request):
    """Global context for templates"""
    from apps.core.models import HomeContent
    contents = {c.key: c for c in HomeContent.objects.filter(is_active=True)}
    result = {'site_contents': contents}
    try:
        from apps.cms.models import IconConfig
        icons = {ic.location: ic for ic in IconConfig.objects.all()}
        result['nav_icons'] = icons
    except Exception:
        result['nav_icons'] = {}
    try:
        from django.db.models import Prefetch
        from apps.core.models import NavItem
        # Ensure Programs has Gallery child (for hover submenu)
        programs = NavItem.objects.filter(url='/programs/', parent__isnull=True).first()
        if programs:
            old = programs.children.filter(url='/programs/gallery/').first()
            if old:
                old.url = '/gallery/'
                old.save()
            if not programs.children.filter(url='/gallery/', is_active=True).exists():
                NavItem.objects.get_or_create(
                    url='/gallery/', parent=programs,
                    defaults={'title': 'Gallery', 'icon_class': 'fas fa-images', 'order': 0, 'is_active': True}
                )
        result['nav_items'] = list(NavItem.objects.filter(is_active=True, parent__isnull=True).prefetch_related(
            Prefetch('children', queryset=NavItem.objects.filter(is_active=True).order_by('order', 'id'))
        ))
    except Exception:
        result['nav_items'] = []
    try:
        from apps.core.models import SiteTheme
        result['site_theme'] = SiteTheme.get()
    except Exception:
        result['site_theme'] = None
    try:
        from apps.core.models import SiteIdentity
        result['site_identity'] = SiteIdentity.get()
    except Exception:
        result['site_identity'] = None
    try:
        from apps.contact.models import ChatSettings
        settings = ChatSettings.get()
        result['chat_settings'] = settings
        try:
            result['admin_chat_online'] = settings.admin_is_online()
        except Exception:
            result['admin_chat_online'] = False
    except Exception:
        result['chat_settings'] = None
        result['admin_chat_online'] = False

    return result
