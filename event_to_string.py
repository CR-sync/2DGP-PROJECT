def event_to_string(state_event):
    """이벤트의 모든 상세 정보를 문자열로 반환 (모든 키 자동 처리)"""
    from pico2d import SDL_KEYDOWN, SDL_KEYUP
    import pico2d

    event_names = {
        SDL_KEYDOWN: 'KEYDOWN',
        SDL_KEYUP: 'KEYUP'
    }

    state_event_type = state_event[0]  # state_event is ('INPUT', event)
    event = state_event[1]  # state_event is ('INPUT', event)
    if state_event_type != 'INPUT':
        return f"{state_event}"

    # pico2d 모듈에서 모든 SDLK_ 상수 자동 수집
    key_names = {}
    for name in dir(pico2d):
        if name.startswith('SDLK_'):
            key_code = getattr(pico2d, name)
            key_name = name.replace('SDLK_', '')
            key_names[key_code] = key_name

    event_type = event_names.get(event.type, f'Unknown({event.type})')
    key_name = key_names.get(event.key, f'key({event.key})')

    info = f'{event_type}:{key_name}'

    # 수정자 키 정보 추가 (Shift, Ctrl, Alt 등)
    if hasattr(event, 'mod') and event.mod:
        info += f', mod={event.mod}'

    return f"('{state_event_type}', {info})"