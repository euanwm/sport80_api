This now supports both BWL and USAW Sport80 pages. I'll write a more detailed readme once i've tidied things up a bit more.

### Simple Test Script

```python
from sport80 import SportEighty

new_funcs = SportEighty("https://bwl.sport80.com")

index_list = new_funcs.event_index(2022)[0]
# {'event': 'Scottish Masters 2022', 'level': 'Tier 2', 'date': '2022-03-19', 'results': 40, 'action': [{'type': 'route_button', 'route': '/public/rankings/results/379', 'text': 'View', 'icon': 'mdi-eye', 'disabled': False, 'confirmation_message': None, 'default_table_row_action': True}]}
event_results = new_funcs.event_results(index_list['action'][0]['route'])
print(event_results)
```
