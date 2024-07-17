from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PacienteUpdateForm

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = PacienteUpdateForm(request.POST, instance=request.user.paciente)
        if form.is_valid():
            form.save()
            return redirect('home_paciente')
    else:
        form = PacienteUpdateForm(instance=request.user.paciente)
    return render(request, 'paciente/actualizar_perfil.html', {'form': form})
