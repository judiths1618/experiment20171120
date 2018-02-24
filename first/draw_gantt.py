import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import gantt_data as g

plotly.tools.set_credentials_file(username='Judiths',
                                  api_key='CTkeLvhRVI0rGFqFfKou')

csv_file = '.\\datafile\\res.csv'
pid_num = g.pid_num(csv_file)
vm_num = g.vm_num(pid_num)
task_num = g.task_num(csv_file)
task = g.task(csv_file)
color_num = g.color_num(task)
setupx = g.setup(csv_file)
min = min(setupx)
setup = [setupx[i] - min for i in range(len(setupx))]
print('Task num: %d VM num: %d' %(len(task), max(vm_num)+1))
print(setup)
duration = g.duration(csv_file)
print(duration)
traces = []


for i in range(len(setup)):
    traces.append(go.Bar(
        y=vm_num[i],
        x=setup[i],
        name=task[i],
        orientation = 'h',
        marker = dict(
            color='rgba(1,1,1, 0.0)',
        )
    ))
    traces.append(go.Bar (
        y=vm_num[i],
        x=setup[i]+duration[i],
        name=task[i],
        orientation='h',
        marker=dict (
            color='rgba(55, 128, 191, 0.7)',
            line=dict (
                color='rgba(55, 128, 191, 1.0)',
                width=2,
            )
        )
    ))

data = traces
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='marker-h-bar')