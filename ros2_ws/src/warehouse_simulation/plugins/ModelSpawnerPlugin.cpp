
#include <ignition/gazebo/System.hh>
#include <ignition/gazebo/Model.hh>
#include <ignition/gazebo/EntityComponentManager.hh>
#include <ignition/gazebo/components/Name.hh>
#include <ignition/gazebo/components/Pose.hh>
#include <ignition/gazebo/components/Static.hh>
#include <ignition/gazebo/components/Model.hh>
#include <ignition/gazebo/Util.hh>
#include <ignition/msgs/EntityFactory.hh>
#include <ignition/transport/Node.hh>
#include <ignition/plugin/Register.hh>

namespace ignition
{
namespace gazebo
{
  class ModelSpawnerPlugin : public System, public ISystemConfigure, public ISystemPreUpdate
  {
    public: void Configure(const Entity &/*_entity*/, const std::shared_ptr<const sdf::Element> &_sdf, EntityComponentManager &/*_ecm*/, EventManager &/*_eventMgr*/) override
    {
      if (_sdf->HasElement("model_name"))
        this->modelName = _sdf->Get<std::string>("model_name");

      if (_sdf->HasElement("spawn_delay"))
        this->spawnDelay = _sdf->Get<double>("spawn_delay");

      this->startTime = std::chrono::steady_clock::now();
    }

    public: void PreUpdate(const UpdateInfo &/*_info*/, EntityComponentManager &/*_ecm*/) override
    {
      auto currentTime = std::chrono::steady_clock::now();
      std::chrono::duration<double> elapsed = currentTime - this->startTime;

      if (elapsed.count() >= this->spawnDelay && !this->modelSpawned)
      {
        ignition::msgs::EntityFactory req;
        req.set_sdf_filename("path/to/fire_generator.sdf");
        this->node.Request("/world/lidar_sensor/create", req);
        this->modelSpawned = true;
      }
    }

    private: std::string modelName;
    private: double spawnDelay{0.0};
    private: std::chrono::steady_clock::time_point startTime;
    private: bool modelSpawned{false};
    private: transport::Node node;
  };
  IGNITION_ADD_PLUGIN(ModelSpawnerPlugin, System, ISystemConfigure, ISystemPreUpdate)
}
}