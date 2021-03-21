from ovito.io import import_file, export_file
from ovito.modifiers import DislocationAnalysisModifier
from ovito.data import DislocationNetwork

pipeline = import_file("input/simulation.dump")

# Extract dislocation lines from a crystal with diamond structure:
modifier = DislocationAnalysisModifier()
modifier.input_crystal_structure = DislocationAnalysisModifier.Lattice.CubicDiamond
pipeline.modifiers.append(modifier)
data = pipeline.compute()

total_line_length = data.attributes['DislocationAnalysis.total_line_length']
cell_volume = data.attributes['DislocationAnalysis.cell_volume']
print("Dislocation density: %f" % (total_line_length / cell_volume))

# Print list of dislocation lines:
print("Found %i dislocation segments" % len(data.dislocations.segments))
for segment in data.dislocations.segments:
    print("Segment %i: length=%f, Burgers vector=%s" % (segment.id, segment.length, segment.true_burgers_vector))
    print(segment.points)

# Export dislocation lines to a CA file:
export_file(pipeline, "output/dislocations.ca", "ca")

# Or export dislocations to a ParaView VTK file:
export_file(pipeline, "output/dislocations.vtk", "vtk/disloc”