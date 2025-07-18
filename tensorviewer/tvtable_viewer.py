from tvlibs import *

class TVTableViewer(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    layout = QVBoxLayout(self)
    self.table_view = QTableView(self)
    self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
    self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    # 
    hlayout = QHBoxLayout()
    hlayout.addWidget(QLabel("Tensor View Index", self))
    self.tensor_view_edit = QLineEdit(self)
    self.tensor_view_edit.returnPressed.connect(self.updateDataView)
    hlayout.addWidget(self.tensor_view_edit)
    self.btn_view = QPushButton("Apply", self)
    self.btn_view.clicked.connect(self.updateDataView)
    hlayout.addWidget(self.btn_view)
    self.btn_reset = QPushButton("Reset", self)
    self.btn_reset.clicked.connect(lambda: self.setData(self.data, self.data_name))
    hlayout.addWidget(self.btn_reset)
    hlayout.addStretch(1)

    layout.addLayout(hlayout)
    layout.addWidget(self.table_view)

    self.status_edit = QLabel(self)
    self.view_edit = QLabel(self)
    layout.addWidget(self.status_edit)
    layout.addWidget(self.view_edit)
    self.setLayout(layout)
    self.data = None
    self.data_name = ""

  def setData(self, data, name=""):
    if isinstance(data, np.ndarray):
      if data.ndim <= 2:
        self._setDataView(data)
        self.tensor_view_edit.setText(f"[{','.join([':'] * data.ndim)}]")
        self.btn_view.setEnabled(False)
      else:
        vs = [':',':']
        for i in range(data.ndim - 2):
          vs.append('0')
        vss = ','.join(vs)
        vss = f'[{vss}]'
        vd = self._createDataView(data, vss)
        self.tensor_view_edit.setText(vss)
        self._setDataView(vd)
        self.btn_view.setEnabled(True)

      self.status_edit.setText(f"Data {name}, shape: {data.shape}, dtype: {data.dtype}")
      self.setWindowTitle(f"Tensor Viewer - {name} ({data.shape})")
      self.data = data
      self.data_name = name
    else:
      raise ValueError("Data must be a numpy ndarray.")
    
  def updateDataView(self):
    if hasattr(self, 'data'):
      view_str = self.tensor_view_edit.text()
      if view_str:
        vd = self._createDataView(self.data, view_str)
        self._setDataView(vd)
      else:
        self._setDataView(self.data)

  def _createDataView(self, data, view_str):
    view_str = view_str.strip()
    view_str = view_str.replace("[", "")
    view_str = view_str.replace("]", "")
    view_str = view_str.replace(" ", "")
    view_tuple = []
    try:
      for v in view_str.split(','):
        if v == ':':
          view_tuple.append(slice(None))
        elif ':' in v:
          vcc = v.split(':')
          if len(vcc) == 2:
            start = int(vcc[0]) if vcc[0] else None
            end = int(vcc[1]) if vcc[1] else None
            view_tuple.append(slice(start, end))
          elif len(vcc) == 3:
            start = int(vcc[0]) if vcc[0] else None
            end = int(vcc[1]) if vcc[1] else None
            step = int(vcc[2]) if vcc[2] else 1
            view_tuple.append(slice(start, end, step))
        else:
          view_tuple.append(int(v))
    except Exception as e:
      QMessageBox.warning(self, "Error", f"Invalid view string: {view_str}\n{str(e)}")
      return None
    index = tuple(view_tuple)
    
    try:
      vd = data[index].copy()
    except Exception as e:
      QMessageBox.warning(self, "Error", f"Failed to create view with index {index}.\n{str(e)}")
      return None
    self.view_edit.setText(f"View: {index}")
    return vd

  def _setDataView(self, data):
    if data is None:
      return
    if isinstance(data, np.ndarray) or isinstance(data, (int, float)):
      tmp_data = None
      if isinstance(data, (int, float)):
        tmp_data = np.array([[data]])
      elif data.ndim == 0:
        tmp_data = np.array([[data.item()]])
      elif data.ndim == 1:
        tmp_data = data.reshape(1, -1)
      elif data.ndim == 2:
        tmp_data = data
      else:
        return

      model = QStandardItemModel(tmp_data.shape[0], tmp_data.shape[1], self)
      for row in range(tmp_data.shape[0]):
        for col in range(tmp_data.shape[1]):
          item = QStandardItem(str(tmp_data[row, col]))
          model.setItem(row, col, item)
      self.table_view.setModel(model)
      model.setHorizontalHeaderLabels([str(i) for i in range(tmp_data.shape[1])])
      model.setVerticalHeaderLabels([str(i) for i in range(tmp_data.shape[0])])
      self.table_view.resizeColumnsToContents()
      self.table_view.resizeRowsToContents()
    else:
      raise ValueError("Data must be a numpy ndarray.")

def CreateViewer(data, name="", parent=None):
    viewer = TVTableViewer(parent)
    viewer.setData(data, name)
    return viewer

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    viewer = TVTableViewer()
    viewer.show()
    viewer.setData(np.random.rand(5,6,7))  # Example data
    sys.exit(app.exec_())