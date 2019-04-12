from google.appengine.ext import ndb

class MyGpu(ndb.Model):
    manufacturer = ndb.StringProperty()
    dateIssued = ndb.StringProperty()
    geometryShader = ndb.BooleanProperty()
    tesselationShader = ndb.BooleanProperty()
    shaderInt16 = ndb.BooleanProperty()
    sparseBinding = ndb.BooleanProperty()
    textureCompressionETC2 = ndb.BooleanProperty()
    vertexPipelineStoresAndAtomics = ndb.BooleanProperty()
