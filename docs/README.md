# Documentation

```python
# serializers.py
from drf_versioned_models.serializers import VersionedModelSerializer

from .models import MyModel, MyModelVersion


class MyModelSerializer(VersionedModelSerializer):
    class Meta:
        model = MyModel
        # TODO: 大概意思是这样，API还需要再设计设计。
        related_model_versions = [
            {
                'model': MyModelVersion, 
                'version_field': 'updated_at',
            }
        ]
```
