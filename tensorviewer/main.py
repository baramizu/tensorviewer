import sys, os
from tvlibs import *



class Sidebar(QWidget):
  item_activated = Signal(str)
  def __init__(self, parent=None):
    super().__init__(parent)
    layout = QVBoxLayout(self)
    self.list = QListWidget()
    layout.addWidget(self.list)
    self.setLayout(layout)
    self.list.setSelectionMode(QAbstractItemView.SingleSelection)
    self.list.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.list.itemClicked.connect(self.on_item_clicked)
  def addItems(self, items):
    self.list.clear()
    for item in items:
      self.list.addItem(item)
  def on_item_clicked(self, item):
    self.item_activated.emit(item.text())
    self.list.clearSelection()
    item.setSelected(True)

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.appName = "Tensor Viewer"
    self.setWindowTitle(self.appName)

    splitter = QSplitter(Qt.Horizontal)
    self.sidebar = Sidebar()
    self.sidebar.item_activated.connect(self.actionActiveSubWindow)
    splitter.addWidget(self.sidebar)

    self.mdi_area = QMdiArea()
    splitter.addWidget(self.mdi_area)
    splitter.setStretchFactor(1, 1)

    self.setCentralWidget(splitter)
    self._create_menu()

    self.sub_windows = {}
    self.tv = {}

  def _create_menu(self):
    menubar = self.menuBar()
    file_menu = menubar.addMenu("File")
    new_action = QAction("Open", self)
    new_action.triggered.connect(self.actionOpenFile)
    file_menu.addAction(new_action)

  def actionOpenFile(self, filename=None):
    if not filename:
      filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Data Files (*.npy *.npz *.csv *.txt *.pt *.pth)")
    if not filename or not os.path.exists(filename):
      return
    import tv_dataloader
    dataset, msg = tv_dataloader.load_data(filename)
    if dataset is None:
      QMessageBox.warning(self, "Error", msg)
      return
    self.setWindowTitle(self.appName + " - " + os.path.basename(filename))
    if isinstance(dataset, np.ndarray):
      dataset = {"data": dataset}
    self.sidebar.addItems(list(dataset.keys()))
    self.dataset = dataset
    return


  def actionActiveSubWindow(self, data_name):
    if data_name in self.sub_windows:
      sub = self.sub_windows[data_name]
      tv = self.tv.get(data_name, None)
      tv.show()
      sub.show()
      sub.activateWindow()
      return
    sub = QMdiSubWindow()
    import tvtable_viewer
    tv = tvtable_viewer.CreateViewer(self.dataset[data_name], data_name, self)
    sub.setWidget(tv)
    self.tv[data_name] = tv
    # sub.setWidgetResizable(True)
    sub.setWindowTitle(data_name)
    self.mdi_area.addSubWindow(sub)
    self.sub_windows[data_name] = sub
    sub.show()

def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.resize(900, 600)
  window.show()
  if len(sys.argv) > 1:
    filename = sys.argv[1]
    window.actionOpenFile(filename)
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()