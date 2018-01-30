{% set users = ['name'] %}
{% for user in users %} 
{{ user }}:
  user.absent:
    - name: {{ user }}
    - purge: True
    - force: True
{% endfor %}
  group.absent:
    - name: dev
