from rest_framework import renderers

class OutBoundDataRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = super().render({
                'errors': data
            })
        else:
            response = super().render({
                'data': data
            })
        return  response