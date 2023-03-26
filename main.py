import pygame, sys, pygame_gui, socket
from simulation.MapLoader import MapLoader
from simulation.Tile import Tile
from aStar.a_star import AStar
from aStar.node import Node


class App:
    def __init__(self):
        pygame.init()
        self._wndResolution = (1000, 600)
        self._wnd           = pygame.display.set_mode(self._wndResolution)
        pygame.display.set_caption("RObocikSimulejtor")
        
        self._guiManager    = pygame_gui.UIManager(self._wndResolution)
        self._uiPanel       = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((800, 0), (300, 800)),  manager=self._guiManager, starting_layer_height=50)

        self._editMapButton         = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 10), (200, 40)),text='Edytuj mape',manager=self._guiManager, container=self._uiPanel)
        self._startPosButton        = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 60), (200, 40)),text='Ustaw start',manager=self._guiManager, container=self._uiPanel)
        self._endPosButton          = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 110), (200, 40)),text='Ustaw koniec',manager=self._guiManager, container=self._uiPanel)
        self._startAStar            = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 160), (200, 40)),text='Wyznacz scieżke',manager=self._guiManager, container=self._uiPanel)
        self._startSimulation       = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 210), (200, 40)),text='Rozpocznij symulacje',manager=self._guiManager, container=self._uiPanel)

        self._viewPath              = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((40, 260), (200, 26)), manager=self._guiManager, container=self._uiPanel, 
                                                                                        item_list = [("Pokaz siciezke", "1")], default_selection=("Pokaz siciezke", "1"))

        self._diagonalJumpsOpt      = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((40, 290), (200, 26)), manager=self._guiManager, container=self._uiPanel, 
                                                                                        item_list = [("Skok po przekątnych", "1")], default_selection=("Skok po przekątnych", "1"))
        
        self._diagonalCorrectionOpt = pygame_gui.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((40, 320), (200, 26)), manager=self._guiManager, container=self._uiPanel, 
                                                                                        item_list = [("Korekcja przekątnych", "1")], default_selection=("Korekcja przekątnych", "1"))
    

        self._robotIp           = "192.168.0.102"
        self._robotPort         = "3333"
        self._robotSocket       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._robotSocketFlag   = False
        
        self._textRobotIp       = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((40, 370), (200, 40),), manager=self._guiManager, container=self._uiPanel, initial_text=self._robotIp)
        self._textRobotPort     = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((40, 420), (200, 40),), manager=self._guiManager, container=self._uiPanel, initial_text=self._robotPort)
        self._btnConnect        = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 470), (200, 40)), manager=self._guiManager, text="Polacz robota", container=self._uiPanel)
        self._btnSendPath       = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 520), (200, 40)), manager=self._guiManager, text="Wyslij dane do robota", container=self._uiPanel)
        self._btnRobotStart     = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 470), (200, 40)), manager=self._guiManager, text="Robot start", container=self._uiPanel)

        self.aStartPath = None

        self.lastClickedPos         = (-1, -1)
        self.mouseIsPressed         = False
        self.editMode               = False
        self._setStartPosMode       = False
        self._setEndPosMode         = False
        self._saveMapOnExit         = True
        self._mapName               = ""
        self._pathExist             = False
        self._showPath              = True
        self._diagonalJump          = True
        self._diagonalCorrextion    = True
        self._simulation            = False
        self._dataIsSendedToRobot   = False
        self._disableMapEditing()

    def _disableMapEditing(self):
        self.editMode           = False
        self._editMapButton.set_text("Włącz edycje mapy")
    def _recalcWindowSize(self):
        tSize = self.map.getTileSize()
        mSize = self.map.getSize()
        offX = self._uiPanel.relative_rect.width
        newWinSize = (tSize[0] * mSize[0] + offX, tSize[1] * mSize[1])

        self._uiPanel.set_relative_position((tSize[0] * mSize[0], 0))
        self._uiPanel.on_locale_changed()
        pygame.display.set_mode(newWinSize)  

    def _processEvents(self, ev):
        if ev.type == pygame.QUIT: 
            if self._saveMapOnExit:
                MapLoader.saveMap(self.map.getMapFileName(), self.map)
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.mouseIsPressed = False
            if self._setStartPosMode:
               self._setStartPosMode = False 
               
            elif self._setStartPosMode:
                self._setStartPosMode = False

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            cords = self.map.calcFromPosToTileNum(ev.pos)
            self.mouseIsPressed = True
            if self.editMode: 
                self._pathExist = False
                self.map.setWallByPos(ev.pos)
            elif self._setStartPosMode:
                self._setStartPosMode = False
                self.map.setStartPos(cords)
            elif self._setEndPosMode:
                self._setEndPosMode = False
                self.map.setEndPos(cords)
            

        elif ev.type == pygame.MOUSEMOTION:
            if self.mouseIsPressed and self.editMode:
                mousePos = ev.pos
                newTilePos = self.map.calcFromPosToTileNum(mousePos)
                if newTilePos != self.lastClickedPos:        
                    self.lastClickedPos = newTilePos
                    self.map.setWallByPos(mousePos)

    def _sendCommandToRobot(self, cmd):
        if self._robotSocketFlag is False:
            print("Robot nie podlaczony!!")
            return
        
        try:
            self._robotSocket.send(str.encode(cmd))
        except OSError as err:
            print("Robot nie podlaczony!!!")
            self._robotSocket.close()
            self._robotSocketFlag = False
            return
        
    def _precessGuiEvents(self, ev):
        if ev.type == pygame_gui.UI_BUTTON_PRESSED:
            if ev.ui_element == self._editMapButton:
                self.robot.stopSimulation()
                self.robot.hideRobot()
                self.editMode = not self.editMode
                if self.editMode:
                    self._setStartPosMode   = False
                    self._setEndPosMode     = False     
                    self._editMapButton.set_text("Wyłącz edycje mapy")
                else:
                    self._editMapButton.set_text("Włącz edycje mapy")
            elif ev.ui_element == self._startPosButton:
                self._pathExist         = False
                self._setStartPosMode   = True
                self._disableMapEditing()
                self.robot.stopSimulation()
                self.robot.hideRobot()
                self._setEndPosMode     = False  
            elif ev.ui_element == self._endPosButton:
                self._pathExist         = False
                self._setEndPosMode     = True
                self._setStartPosMode   = False
                self._disableMapEditing()
                self.robot.stopSimulation()
                self.robot.hideRobot()
            elif ev.ui_element == self._startAStar:
                star = AStar(self.map.map, self.map.getSize())
                star.diagonalJump(self._diagonalJump)
                star.diagolnalCorrection(self._diagonalCorrextion)
                self.path       = star.findPath2(Node(self.map.getStartCords()), Node((self.map.getEndCords())))
                self._pathExist = True
                self.robot.stopSimulation()
                self.robot.hideRobot()
            elif ev.ui_element == self._startSimulation:
                if self._pathExist == False:
                    star = AStar(self.map.map, self.map.getSize())
                    star.diagonalJump(self._diagonalJump)
                    star.diagolnalCorrection(self._diagonalCorrextion)
                    self.path       = star.findPath2(Node(self.map.getStartCords()), Node((self.map.getEndCords())))
                    self._pathExist = True
                    
                self.robot.setPath(self.path)
                self.robot.startSimulation()
                print("====Symulacja.......")
            elif ev.ui_element == self._btnConnect:
                if self._robotSocketFlag is True:
                    self._robotSocket.close()
                print(f"Laczenie z robotem {(self._textRobotIp.get_text(), int(self._textRobotPort.get_text()))}")
                self._robotSocket.settimeout(1)
                try:
                    self._robotSocket.connect((self._textRobotIp.get_text(), int(self._textRobotPort.get_text())))
                    self._robotSocketFlag = True
                    self._sendCommandToRobot("ping")
                    self._sendCommandToRobot("setMode auto")
                    print("Podlaczono!!!")
                except Exception as err:
                    self._robotSocketFlag = False
                    print(f"Blad polaczenia z robotem")
                    print(err)
            elif ev.ui_element == self._btnSendPath:
                if self._pathExist and self._robotSocketFlag:
                    self._sendCommandToRobot("setMode auto")
                    
                    self._dataIsSendedToRobot = True
                    
                    #send data to robot
                else:
                    print("Robot nie podlaczony lub nie ma sciezki!!!")
            elif ev.ui_element == self._btnRobotStart:
                if self._dataIsSendedToRobot:
                    #robot start
                    self._sendCommandToRobot("start")
                else:
                    print("nie wyslano sciezki!!!") 
                    
                
        elif ev.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if ev.ui_element == self._viewPath:
                self._showPath = True
            elif ev.ui_element == self._diagonalJumpsOpt:
                self._diagonalJump = True
            elif ev.ui_element == self._diagonalCorrectionOpt:
                self._diagonalCorrextion = True
        elif ev.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
            if ev.ui_element == self._viewPath:
                self._showPath = False
            elif ev.ui_element == self._diagonalJumpsOpt:
                self._diagonalJump = False 
            elif ev.ui_element == self._diagonalCorrectionOpt:
                self._diagonalCorrextion = False
            
    def main(self):     
        bg = 0, 0, 0
        (self.map, self.robot) = MapLoader.fromJson("maps/m02.json")

        self._recalcWindowSize()
        mainClock = pygame.time.Clock()

        while True:
            deltaTime = mainClock.tick(60)/1000

            for ev in pygame.event.get():
                self._processEvents(ev)
                self._guiManager.process_events(ev)
                self._precessGuiEvents(ev)

            self._guiManager.update(deltaTime)

            self._wnd.fill(bg)
            self.map.draw(self._wnd)

            if self._pathExist and self._showPath:
                self.map.drawPath(self._wnd, self.path)
            
            self.robot.update(deltaTime)
            self.robot.draw(self._wnd)
            
            self._guiManager.draw_ui(self._wnd)
            pygame.display.update()

if __name__ == '__main__':
    app = App()
    app.main()