from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect

#Clases para Acceso a niveles de usuario:

#clase para el LoginRequired
class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


#clase para acceso del superusuario
class SuperUserMixinRequired(object):
	"""Nivel de usuario super User"""
	def dispatch(self,request,*args,**kwargs):
		print (request.user.is_superuser)
		if not request.user.is_superuser:
			return redirect(reverse_lazy('core:prohibido'))
		return super(SuperUserMixinRequired,self).dispatch(request,*args,**kwargs)


#clase para acceso de staff
class StaffMixinRequired(object):
	"""Nivel de usuario super User"""
	def dispatch(self,request,*args,**kwargs):
		print (request.user.is_staff)
		if not request.user.is_staff:
			return redirect(reverse_lazy('login'))
		return super(StaffMixinRequired,self).dispatch(request,*args,**kwargs)