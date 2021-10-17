def smart_truncate(content, length=120, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix
