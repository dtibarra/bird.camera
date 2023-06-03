from jinja2 import Environment, FileSystemLoader
import yaml
with open("products.yaml", "r+") as file:
    data = yaml.safe_load(file)
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('store.html')
    output = template.render(data)
print(output)