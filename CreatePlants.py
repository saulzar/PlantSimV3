import geoplantrep as PG
import VTK_PlantRendering.ConvertToVTKPlant as CVVTK
import VTK_PlantRendering.DisplayVTKPlant as DP
import PlantGeneration.GenerateStemStructure as GStem
import PlantGeneration.Generate2DTriStructures as G2D
import PlantGeneration.Generate3DTriStructures as G3D


# TODO: Stem radius based on height/stem length
# TODO: make fully vtk free leaf generator
# TODO: Polydata noise addition and smoothing
# TODO: Leaf-stem merge for plant generation
# TODO: Surface texturing
# TODO: Surface reflectivity
# TODO: Shadows
# TODO: Plant movement, growth


LOCAL_HOME_PATH = '/local/'
OUTDIR_PATH = LOCAL_HOME_PATH + 'Dropbox/PlantSimData/'


DISPLAY_PLANT_SAMPLES = True
LOAD_PLANT = False
SAVE_PLANT = False

rep_plant = PG.PlantData()
vtk_plant_list = []

if LOAD_PLANT:
    rep_plant = PG.PlantData()
    rep_plant.LoadPlantFile('test_save.plant')
    vtk_plant = CVVTK.vtkPlantData(rep_plant)
    vtk_plant.BuildComponents()
    vtk_plant.SetActorPostions()
    vtk_plant_list.append(vtk_plant)
else:
    for plant_c in range(6):
        for plant_r in range(2):
            # Generate Randomised plant using a combination of algorithms
            rep_plant = PG.PlantData()
            GStem.GenRandSplineStem(rep_plant, 30)
            end_stem_indxs = GStem.FindEndSegIndxs(rep_plant)
            G2D.GenRandLeaves(rep_plant, end_stem_indxs)
            #G3D.GenRandFruit(rep_plant)

            vtk_plant = CVVTK.vtkPlantData(rep_plant)
            vtk_plant.BuildComponents()
            vtk_plant.SetActorPostions(offset=[0.2 * plant_c, 0, 0.2 * plant_r])
            vtk_plant_list.append(vtk_plant)


plant_display = DP.plantVTKDataDisplay(vtk_plant_list)
plant_display.InitRenderWindow( axes_on=False, bkgnd=[0.8, 0.8, 0.8], res_x=1920, res_y=1080 )
plant_display.InitBackground(disp_pots=True)
plant_display.AddActors()
plant_display.InitInteractor()
plant_display.InitLighting(mode=0)
plant_display.RenderPlant()

if SAVE_PLANT:
    rep_plant.SavePlantFile('test_save.plant')