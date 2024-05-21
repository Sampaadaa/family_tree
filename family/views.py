from django.shortcuts import render
from family.models import Person, Relationship
import graphviz
from collections import defaultdict
import base64
from io import BytesIO

def family_tree(request):
    # Fetch all people
    people = Person.objects.all()

    # Fetch all relationships
    relationships = Relationship.objects.all()

    # Initialize a new directed graph
    dot = graphviz.Digraph(comment='Family Tree')
    dot.attr(rankdir='TB')  # Optional: to make the graph vertical

    # Add nodes for each person
    for person in people:
        dot.node(str(person.id), f"{person.first_name} {person.last_name}")

    # Dictionary to store children with multiple parents
    child_to_parents = defaultdict(list)

    # Populate child_to_parents dictionary
    for relationship in relationships:
        child_to_parents[relationship.child.id].append(relationship.parent.id)

    # Add edges for each relationship
    for child_id, parent_ids in child_to_parents.items():
        if len(parent_ids) > 1:
            # Create a subgraph for the union of parents
            with dot.subgraph() as s:
                s.attr(rank='same')  # Ensure parents are on the same rank (horizontal alignment)

                # Create an invisible node for the marriage
                marriage_node_id = f"marriage_{child_id}"
                s.node(marriage_node_id, shape="point", width="0")

                # Connect parents to the marriage node with horizontal lines
                parent_nodes = []
                for parent_id in parent_ids:
                    parent_nodes.append(str(parent_id))

                s.edge(parent_nodes[0], marriage_node_id, style="invis")  # Invisible edge to align parents
                for parent_id in parent_nodes:
                    s.edge(parent_id, marriage_node_id, style="solid")

                # Connect the marriage node to the child
                dot.edge(marriage_node_id, str(child_id))
        else:
            # Single parent case
            parent_id = parent_ids[0]
            dot.edge(str(parent_id), str(child_id))

    # Render the graph to PNG image data
    png_data = dot.pipe(format='png')

    # Encode the PNG data as base64
    base64_png = base64.b64encode(png_data).decode('utf-8')

    # Pass the base64-encoded PNG data to the template
    context = {'image_data': base64_png}
    return render(request, 'family.html', context)
